from django.shortcuts import render
from reservation.models import *
import json, requests, time, datetime
from datetime import date
from django.utils.html import strip_tags
from django.http import HttpResponse
from multiprocessing import Process
import pdfcrowd

#get reservation from S2M API
def get_s2m_res(request):
    url = 'http://www.seats2meet.com/api/reservation//%s' % request.GET.get('r', '')
    headers = {'content-type':'application/json'}
    data = {
    "ApiKey":91216637,
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
    "ApiKey":91216637,
    "AuthorizedProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    "LanguageId": 65,
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
    "ApiKey":91216637,
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
    "ApiKey":91216637,
    "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    "locationId": location,
    }
      
    r = requests.get(url, params=json.dumps(data), headers=headers)
    r = json.loads(r.text)
    
    return r

        
        


def show(request):
    # default to your native language
    request.session['lang'] = request.GET.get('lang', 'en')
    
    if request.GET.get('pdf') == 'yes':
        try:
            # create an API client instance
            client = pdfcrowd.Client("donfelicio", "c80838c2ded070c41bcf39c0a619c809")
            
            full_path = ('http', ('', 's')[request.is_secure()], '://', request.META['HTTP_HOST'], request.get_full_path())
            # convert a web page and store the generated PDF to a variable
            pdf = client.convertURI(''.join(full_path).split("&pdf=yes")[0])
            pdf = client.setPageWidth("298mm") 
    
             # set HTTP response headers
            response = HttpResponse(content_type="application/pdf")
            response["Cache-Control"] = "max-age=0"
            response["Accept-Ranges"] = "none"
            response["Content-Disposition"] = "attachment; filename=google_com.pdf"
    
            # send the generated PDF
            response.write(pdf)
        except pdfcrowd.Error, why:
            response = HttpResponse(content_type="text/plain")
            response.write(why)
        return response
        
    reservation = get_s2m_res(request)
    offer_duration = datetime.datetime.strptime(str(reservation.get("CreatedOn").split("T")[0]), '%Y-%m-%d') + datetime.timedelta(days=14)
    startdate = datetime.datetime.strptime(str(reservation.get("StartTime").split("T")[0]), '%Y-%m-%d')
    enddate =  datetime.datetime.strptime(str(reservation.get("EndTime").split("T")[0]), '%Y-%m-%d')
    
    context={
        'reservation': reservation,
        'intro_text': Reservation.objects.get(res_id=reservation.get("Id")).res_intro,
        'startdate': startdate.strftime('%d-%b-%Y'),
        'offer_duration': offer_duration.strftime('%d-%b-%Y'), 
        'starttime': "%s:%s" % (reservation.get("StartTime").split("T")[1].split(':')[0], reservation.get("StartTime").split("T")[1].split(':')[1]),
        'enddate': enddate.strftime('%d-%b-%Y'),
        'endtime':  "%s:%s" % (reservation.get("EndTime").split("T")[1].split(':')[0], reservation.get("EndTime").split("T")[1].split(':')[1]),
        'meetingspaces': get_s2m_meetingspaces(request, reservation.get("LocationId")),
        'profile': get_s2m_profile(request),
        'location': get_s2m_address(request, reservation.get("LocationId")),
        }
    if request.GET.get('pdf') == 'yes':
        context['pdf_printing'] = 'yes'
    if reservation.get("TotalSeats") != 0:
        context['price_per_person'] = reservation.get("TotalExcl") / reservation.get("TotalSeats")
        
    template="show.html"
    return render(request, template, context)

