from django.shortcuts import render
from reservation.models import *
import json, requests, time
from datetime import date
from django.utils.html import strip_tags

#get reservation from S2M API
def get_s2m_res(request):
    url = 'http://www.seats2meet.com/api/reservation//%s' % request.GET.get('r', '')
    headers = {'content-type':'application/json'}
    data = {
    "ApiKey":14257895,
    "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    }
      
    r = requests.get(url, params=json.dumps(data), headers=headers)
    r = json.loads(r.text)
    
    return r

#get meetingspaces from S2M API
def get_s2m_meetingspaces(request, location):
    url = 'http://www.seats2meet.com/api/unit/meetingspaces/%s' % location
    headers = {'content-type':'application/json'}
    data = {
    "locationId": location,
    "ApiKey":14257895,
    "AuthorizedProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    "LanguageId": 3,
    "SearchTerm": "",
    "Page": 1,
    "ItemsPerPage": 50
    }
      
    r = requests.get(url, params=json.dumps(data), headers=headers)
    r = json.loads(r.text)
    
    return r

#get user of sender
def get_s2m_profile(request):
    url = 'http://www.seats2meet.com/api/profiles/getbykey/%s' % request.GET.get('u', '')
    headers = {'content-type':'application/json'}
    data = {
    "profileKey": request.GET.get('u', ''),
    "ApiKey":14257895,
    "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    }
      
    r = requests.get(url, params=json.dumps(data), headers=headers)
    r = json.loads(r.text)
    
    return r


#get directions to location
def get_s2m_address(request, location):
    url = 'http://www.seats2meet.com/api/locations/%s' % location
    headers = {'content-type':'application/json'}
    data = {
    "ApiKey":14257895,
    "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    "locationId": location,
    }
      
    r = requests.get(url, params=json.dumps(data), headers=headers)
    r = json.loads(r.text)
    
    return r

#get option details
def get_s2m_options(request, resid):
    url = 'http://www.seats2meet.com/api/reservation/wizard/options/%s' % resid
    headers = {'content-type':'application/json'}
    data = {
    "ApiKey":14257895,
    "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    "ReservationId": resid,
    }
      
    r = requests.get(url, params=json.dumps(data), headers=headers)
    r = json.loads(r.text)
    
    return r








def show(request):
        
    reservation = get_s2m_res(request)
            
    #get the res id from the url
    context={
        'reservation': reservation,
        'startdate': reservation.get("StartTime").split("T")[0],
        'starttime': "%s:%s" % (reservation.get("StartTime").split("T")[1].split(':')[0], reservation.get("StartTime").split("T")[1].split(':')[1]),
        'enddate': reservation.get("EndTime").split("T")[0],
        'endtime':  "%s:%s" % (reservation.get("EndTime").split("T")[1].split(':')[0], reservation.get("EndTime").split("T")[1].split(':')[1]),
        'meetingspaces': get_s2m_meetingspaces(request, reservation.get("LocationId")),
        'profile': get_s2m_profile(request),
        'location': get_s2m_address(request, reservation.get("LocationId")),
        'options': strip_tags(get_s2m_options(request, reservation.get("Id")))
        }
    if reservation.get("TotalSeats") != 0:
        context['price_per_person'] = reservation.get("TotalExcl") / reservation.get("TotalSeats")

    template="show.html"
    return render(request, template, context)