from django.shortcuts import render, redirect
from reservation.models import *
from reservation.forms import *
from .s2m import *




def home(request):
    
    url = 'https://apiv2.seats2meet.com/api/locations/profile/6DE79403-D5EF-186C-9529-25ED04A66FD6'
    headers = {'content-type':'application/json'}
    data = {
    "ApiKey":91216637,
    "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    "profileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    }

    r = requests.get(url, data=json.dumps(data), headers=headers)
    print r.url
    r = json.loads(r.text)
        
    
    context={}
    template="test.html"
    return render(request, template, context)
