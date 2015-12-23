from django.shortcuts import render
from reservation.models import *
import json, requests, time, datetime
from datetime import date
from django.utils.html import strip_tags
from django.http import HttpResponse
from multiprocessing import Process
from reservation.s2m import *
from django.core.mail import send_mail
from snippets import *


def show(request):
    #if user sent the offer, send it
    if request.method == "POST" and 'send_to' in request.POST:
        send_mail(request.POST['send_subject'],
        request.POST['send_message'],
        request.POST['send_from'],
        [request.POST['send_to']], fail_silently=False)
        
    #if user adds tekst, add it here
    if request.method == "POST" and 'add_intro' in request.POST:
        instance=Reservation.objects.get(res_id=request.POST['res_id'])
        instance.res_intro = request.POST['intro_text']
        instance.save()
    
    reservation = get_s2m_res_single(request, None)
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
        'profile_to': get_s2m_profile_by_id(request, reservation.get("ProfileId")),
        'location': get_s2m_address(request, reservation.get("LocationId")),
        }
    
    if reservation.get('LanguageId') == 52:
        context['snippets'] = get_snippets('nl')
    else:
        context['snippets'] = get_snippets('en')
    if request.GET.get('pdf') == 'yes':
        context['pdf_printing'] = 'yes'

    if reservation.get("TotalSeats") != 0:
        context['price_per_person'] = reservation.get("TotalExcl") / reservation.get("TotalSeats")

    template="show/showv2.html"
    return render(request, template, context)

