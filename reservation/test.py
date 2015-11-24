from django.shortcuts import render, redirect
from reservation.models import *
from reservation.forms import *
from .s2m import *


def home(request):
   #Let user add input to offer site
   
   print request.POST
   
   context={
     }
   template="test.html"
   return render(request, template, context)


