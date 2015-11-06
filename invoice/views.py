from django.core.management.base import BaseCommand
from django.shortcuts import render
import time, datetime, json, requests
from datetime import date
from django.shortcuts import redirect, render
from reservation.models import *
from invoice.models import *
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives


def home(request):
    # url = 'http://www.seats2meet.com/api/invoices/108601'
    # headers = {'content-type':'application/json', 'Connection':'close'}
    # data = {
    # "ApiKey":91216637,
    # "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    # "LocationId":"563",
    # }
    # r = requests.get(url, params=json.dumps(data), headers=headers)
    # print r.text
    # r = json.loads(r.text) 
    # return r
    # 

    #NB: rowsleft doesn't work here, API doesn't show rows but a count of all items. 
    page = 1
    items = 20
    itemsleft = 100000
    results=[]
    while itemsleft > -20:
        url = 'http://www.seats2meet.com/api/invoices/location/563'
        headers = {'content-type':'application/json', 'Connection':'close'}
        data = {
        "ApiKey":91216637,
        "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
        "StartDate":str(datetime.date.today() - datetime.timedelta(weeks=156)),
        "EndDate":str(datetime.date.today()),
        "SearchTerm":"",
        "StatusIds":[],
        "UnPaidOnly":True,
        "IsDeposit":False,
        "LocationId":"563",
        "Page": page,
        "ItemsPerPage": items
        }
      
        r = requests.get(url, params=json.dumps(data), headers=headers)
        r = json.loads(r.text)
        results.extend(r)
        #up page 1
        page += 1
        
        if itemsleft == 100000:
            for var in r[:1]:
                itemsleft = var.get("MoreRows")
        else:
           itemsleft -= items
        print itemsleft
    print results   
    return results
