import json, requests, datetime
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from multiprocessing import Process
from django.db import connection

#all s2m api requests

def get_location_id(request):
   connection.close()
   #get the location id from the userprofile of logged in user
   return Userprofile.objects.get(user_name=request.user.username).active_location

def get_user_key(request):
   connection.close()
   #get the location id from the userprofile of logged in user
   return Userprofile.objects.get(user_name=request.user.username).user_key
         
#get reservations from S2M API
def get_s2m_res(request): #you should only do this in background, or when user presses refresh, and then still in background with alert 'this might take a minute'. 
   connection.close()
   #set datetime for future date set
   #!!!!WHEN going live, parse all data in rows. Uncomment below to do all.
   page = 1 #!!!!change to 1 after testen
   rowsleft = 100000 #must define but can't be zero:)
   results=[]
   while rowsleft != 0:
   #!!!PRINT NOG DUBBEL, maar alleen bij tweede run. alleen in zelfde browser na refresh van /load. zal wel request onthouden. 
      today = datetime.date.today()
      one_year = datetime.timedelta(weeks=52)
      url = 'http://www.seats2meet.com/api/reservation/location/%s' % get_location_id(request)
      headers = {'content-type':'application/json'}
      data = {
      "ApiKey":14257895,
      "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
      "ChannelId":0,
      "ProfileId":0,
      "CompanyId":0,
      "StatusIds":[1,2,3],
      "MeetingTypeIds":[1],
      "StartDate":str(today),
      "EndDate":str(today + one_year),
      "SearchTerm":"",
      "ShowNoInvoice":False,
      "ShowNoRevenue":True,
      "ShowAmountOpen":False,
      "ShowOptionCategory":-1,
      "Page":page,
      "ItemsPerPage":50
      }
      
      r = requests.get(url, params=json.dumps(data), headers=headers)
      r = json.loads(r.text)
      results.extend(r)
      #up page 1
      page += 1
      
      for var in r[:1]:
         rowsleft = var.get("MoreRows")
         print rowsleft
   return results

   

def s2m_login(request):
   connection.close()
   today = datetime.date.today()
   url = 'https://www.seats2meet.com/api/login'
   headers = {'content-type':'application/json'}
   data = {
   "ApiKey":14257895,
   "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
   "UserName": request.POST["username"],
   "Password": request.POST["pass"]
   }
   
   r = requests.post(url, data=json.dumps(data), headers=headers)
   r = json.loads(r.text)
   
   get_user_key = r.get("Key")
   
   #now get or create the user
   user, created = User.objects.get_or_create(username=r.get("UserName"), email=r.get("Email"), first_name=r.get("FirstName"), last_name=r.get("LastName"))
   #now also create the userprofile to store the key that we often use
   profile = Userprofile.objects.get_or_create(user_name=r.get("UserName"), user_key=r.get("Key"))
   if created is False: #user exists, just log in and redirect. 
      #and now login the user into the Django account
      user.backend = 'django.contrib.auth.backends.ModelBackend'
      login(request, user)

      
      #delete all the users old hidereservation keys (older than today)
      hideres_list = Hidereservation.objects.all().filter(user_name=request.user.username)

      for hideres in hideres_list:
         if hideres.hide_days < today:
            hideres_to_remove = Hidereservation.objects.get(res_id=hideres.res_id, user_name=hideres.user_name)
            hideres_to_remove.delete()
        
      #now check if there's just one location or more, and let the user select one
    
   else: #user is created, log in django and then get the locations
      user.backend = 'django.contrib.auth.backends.ModelBackend'
      login(request, user)
      

def s2m_logout(request):
    logout(request)
    request.session.flush()

def s2m_locationlist():
    connection.close()
    
    url = 'https://www.seats2meet.com/api/locations'
    headers = {'content-type':'application/json'}
    data = {
    "ApiKey":14257895,
    "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    }
    
    r = requests.post(url, data=json.dumps(data), headers=headers)
    r = json.loads(r.text)
    return r
   


 
