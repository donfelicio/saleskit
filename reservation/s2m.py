import json, requests, datetime
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from multiprocessing import Process
from django.db import connection
from django.http import HttpResponse

#all s2m api requests

def get_location_id(request):
   connection.close()
   #get the location id from the userprofile of logged in user
   return Userprofile.objects.get(user_name=request.user.username).active_location

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
      "StartDate":str(datetime.date.today()),
      "EndDate":str(datetime.date.today() + datetime.timedelta(weeks=52)),
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
   if r.status_code == 200:   
      r = json.loads(r.text)
      
      #now get or create the user
      user, created = User.objects.get_or_create(username=r.get("UserName"), email=r.get("Email"), first_name=r.get("FirstName"), last_name=r.get("LastName"))
      #now also create the userprofile to store the key that we often use
      profile = Userprofile.objects.get_or_create(user_name=r.get("UserName"), user_key=r.get("Key"))
      if created is False: #user exists, just log in and redirect. 
         #and now login the user into the Django account
         user.backend = 'django.contrib.auth.backends.ModelBackend'
         login(request, user)
         #and save login date
         instance, created = Userprofile.objects.get_or_create(user_name=request.user.username)
         instance.save()
         #and create login log instance
         Loginlog.objects.create(user_name=request.user.username)

         #delete all the users old hidereservation keys (older than today)   
         for resfilter in Reservationfilter.objects.all().filter(user_name=request.user.username):
            if resfilter.hide_days < today:
               Reservationfilter.objects.get(res_id=resfilter.res_id, user_name=resfilter.user_name).delete()
           
         #now check if there's just one location or more, and let the user select one
       
      else: #user is created, log in django and then get the locations
         user.backend = 'django.contrib.auth.backends.ModelBackend'
         login(request, user)
         #and save login date
         instance, created = Userprofile.objects.get_or_create(user_name=request.user.username)
         instance.save()
         #and create login log instance
         Loginlog.objects.create(user_name=request.user.username)
   else:
      return redirect('/')
      

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
   


 
