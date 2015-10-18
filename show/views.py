from django.shortcuts import render
from reservation.models import *
from reservation.s2m import *

def show(request):
    #get the res id from the url
    context={}
    template="show.html"
    return render(request, template, context)