from django.shortcuts import render, redirect
from reservation.models import *
from reservation.forms import *
from .s2m import *




def home(request):
    
    res_list = Reservation.objects.all().filter(res_location_id=Userprofile.objects.get(user_name=request.user.username).active_location).exclude(reservationfilter__isnull=False, reservationfilter__user_name=request.user.username).exclude(reservationfilter__isnull=False, res_status_sales='6').exclude(res_status_sales='8').exclude(res_status_sales='9').exclude(res_status_sales='10') 
    for reservation in res_list:
        if reservation.res_total_seats < "50" and reservation.res_status_sales == "1":
            print reservation.res_date - datetime.timedelta(weeks=4)
            now_plus_hour = datetime.datetime.strptime('00:00', '%H:%M')
            Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=reservation.res_id), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=(reservation.res_date - datetime.timedelta(weeks=4)), hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))
    
    context={}
    template="test.html"
    return render(request, template, context)
