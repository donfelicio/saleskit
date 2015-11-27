from django.shortcuts import render, redirect
from reservation.models import *
from reservation.forms import *
from .s2m import *


def s2m_locationlist(request):    
    url = 'https://apiv2.seats2meet.com/api/locations/profile/6DE79403-D5EF-186C-9529-25ED04A66FD6'
    headers = {'content-type':'application/json'}
    data = {
    "ApiKey":91216637,
    "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    }
    
    r = requests.get(url, params=json.dumps(data), headers=headers)
    print r.text
    r = json.loads(r.text)
    return r



def home(request):
    
    s2m_locationlist(request)
    
    context={}
    template="test.html"
    return render(request, template, context)
