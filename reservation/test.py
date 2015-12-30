from django.shortcuts import render, redirect
from reservation.models import *
from reservation.forms import *
from .s2m import *




def home(request):

        
    print 'test'
    
    context={}
    template="test.html"
    return render(request, template, context)
