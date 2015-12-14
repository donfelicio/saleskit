import json, requests, datetime
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from multiprocessing import Process
from django.http import HttpResponse

#all s2m api requests

#get reservation list from S2M API
def get_s2m_res(request): #you should only do this in background, or when user presses refresh, and then still in background with alert 'this might take a minute'. 
   page = 1 #!!!!change to 1 after testen
   rowsleft = 100000 #must define but can't be zero:)
   results=[]
   while rowsleft > 0:
      url = 'https://apiv2.seats2meet.com/api/reservation/location/%s' % Userprofile.objects.get(user_name=request.user.username).active_location
      headers = {'content-type':'application/json', 'Connection':'close'}
      data = {
      "ApiKey":91216637,
      "ProfileKey":Userprofile.objects.get(user_name=request.user.username).user_key,
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
      "ItemsPerPage":10
      }
      
      r = requests.get(url, params=json.dumps(data), headers=headers)
      r = json.loads(r.text)
      results.extend(r)
      #up page 1
      page += 1
      
      if rowsleft == 100000:
         for var in r[:1]:
            rowsleft = var.get("MoreRows")
      else:
         rowsleft -= 1
      print rowsleft      

   return results


#UPDATE-API
def get_s2m_res_updated(): #get all CreatedOn and UpdatedOn where date >= today
   page = 1 #!!!!change to 1 after testen
   rowsleft = 100000 #must define but can't be zero:)
   results=[]
   while rowsleft > 0:
      url = 'https://apiv2.seats2meet.com/api/reservation/location/%s' % Userprofile.objects.get(user_name=request.user.username).active_location
      headers = {'content-type':'application/json', 'Connection':'close'}
      data = {
      "ApiKey":91216637,
      "ProfileKey":Userprofile.objects.get(user_name=request.user.username).user_key,
      "ChannelId":0,
      "ProfileId":0,
      "CompanyId":0,
      "StatusIds":[1,2,3],
      "MeetingTypeIds":[1],
      "StartDate":str(datetime.date.today()),
      "EndDate":str(datetime.date.today() + datetime.timedelta(weeks=52)),
      "ChangeDate":str(datetime.date.today()),
      "SearchTerm":"",
      "ShowNoInvoice":False,
      "ShowNoRevenue":True,
      "ShowAmountOpen":False,
      "ShowOptionCategory":-1,
      "Page":page,
      "ItemsPerPage":10
      }
      
      r = requests.get(url, params=json.dumps(data), headers=headers)
      r = json.loads(r.text)
      results.extend(r)
      #up page 1
      page += 1
      
      if rowsleft == 100000:
         for var in r[:1]:
            rowsleft = var.get("MoreRows")
      else:
         rowsleft -= 1
      print rowsleft      

   return results



   

def s2m_login(request):
   today = datetime.date.today()
   url = 'https://apiv2.seats2meet.com/api/login'
   headers = {'content-type':'application/json', 'Connection':'close'}
   data = {
   "ApiKey":91216637,
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
    
    url = 'https://apiv2.seats2meet.com/api/locations'
    headers = {'content-type':'application/json'}
    data = {
    "ApiKey":91216637,
    }
    
    r = requests.post(url, data=json.dumps(data), headers=headers)
    r = json.loads(r.text)
    return r
   
#get reservation from S2M API
def get_s2m_res_single(request, res_id):
   if res_id == None:
      url = 'https://apiv2.seats2meet.com/api/reservation/%s' % request.GET.get('r', '')
   else:
      url = 'https://apiv2.seats2meet.com/api/reservation/%s' % res_id
   headers = {'content-type':'application/json'}
   data = {
   "ApiKey":91216637,

   }
     
   r = requests.get(url, params=json.dumps(data), headers=headers)
   r = json.loads(r.text)
   return r

#get reservation revisions from S2M API
def get_s2m_res_single_revisions(request, res_id):
   url = 'https://apiv2.seats2meet.com/api/reservation/revisions/%s' % res_id
   headers = {'content-type':'application/json'}
   data = {
   "ApiKey":91216637,
   "ProfileKey":Userprofile.objects.get(user_name=request.user.username).user_key,
   }

   r = requests.get(url, params=json.dumps(data), headers=headers)
   r = json.loads(r.text)
   return r

#get meetingspaces from S2M API
def get_s2m_meetingspaces(request, location):
    url = 'https://apiv2.seats2meet.com/api/unit/meetingspaces/%s' % location
    headers = {'content-type':'application/json'}
    data = {
    "locationId": location,
    "ApiKey":91216637,
    "AuthorizedProfileKey":request.GET.get('u', ''),
    "LanguageId": 65,
    "SearchTerm": "",
    "Page": 1,
    "ItemsPerPage": 50
    }
      
    r = requests.get(url, params=json.dumps(data), headers=headers)
    r = json.loads(r.text)
    return r

#get profile of sender by key
def get_s2m_profile(request):
    url = 'https://apiv2.seats2meet.com/api/profiles/getbykey/%s' % request.GET.get('u', '')
    headers = {'content-type':'application/json'}
    data = {
    "profileKey": request.GET.get('u', ''),
    "ApiKey":91216637,
    "ProfileKey":request.GET.get('u', ''),
    }
      
    r = requests.get(url, params=json.dumps(data), headers=headers)
    r = json.loads(r.text)
    
    return r


#get profile by id
def get_s2m_profile_by_id(request, profile_id):
    url = 'https://apiv2.seats2meet.com/api/profiles/getbyid/%s' % profile_id
    headers = {'content-type':'application/json'}
    data = {
    "profileId": profile_id,
    "ApiKey":91216637,
    }
      
    r = requests.get(url, params=json.dumps(data), headers=headers)
    r = json.loads(r.text)
    
    return r
   
   

#get directions to location
def get_s2m_address(request, location):
    url = 'https://apiv2.seats2meet.com/api/locations/%s' % location
    headers = {'content-type':'application/json'}
    data = {
    "ApiKey":91216637,
    "locationId": location,
    }
      
    r = requests.get(url, params=json.dumps(data), headers=headers)
    r = json.loads(r.text)
    
    return r

 
