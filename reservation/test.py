from django.shortcuts import render, redirect
from reservation.models import *
from reservation.forms import *
from .s2m import *




def home(request):
    
    res_list =  Reservationfilter.objects.all()
        
    
    context={'reslist': res_list}
    template="test.html"
    return render(request, template, context)
