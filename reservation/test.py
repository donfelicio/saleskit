from django.shortcuts import render, redirect
from reservation.models import *
from reservation.forms import *
from .s2m import *

def s2m_send_invoice(request):
   url = 'https://www.seats2meet.com/api/invoices/sendmail'
   headers = {'content-type':'application/json; charset-utf-8'}
   data = {
   "ApiKey":91216637,
   "ProfileKey": "6DE79403-D5EF-186C-9529-25ED04A66FD6",
   #"ProfileKey":Userprofile.objects.get(user_name=request.user.username).user_key,
   "InvoiceId": 112719,
   "ChannelId": 0,
   "FromEmail": "felix@meetberlage.com",
   "ToEmail": "felix@donfelicio.com",
   "Cc":"",
   "Subject": "test: invoices",
   "MailText": "test: invoice tekst",
   "Attachement": "", #Invoice_id.pdf
   "IncludeComments": False,
   "LocationId": 563,
   }
 
   # r = requests.post(url, data=json.dumps(data), headers=headers)
   # print r
   # return r


def home(request):
   #Let user add input to offer site
   
   s2m_send_invoice(request)
   
   context={
     }
   template="test.html"
   return render(request, template, context)


