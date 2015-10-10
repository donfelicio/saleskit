from django.shortcuts import render, redirect
from reservation.models import *
from reservation.forms import *
import json, requests, datetime
from .filters import *

#er ging iets mis bij url /?accordion-234 ... of zo, hoe komt dat daar?

#get reservations from S2M API
def get_s2m_res(amount):
   
   #set datetime for future date set
   today = datetime.date.today()
   one_year = datetime.timedelta(weeks=52)
   url = 'https://seats2meet.com/api/reservation/location/563'
   headers = {'content-type':'application/json; charset=utf-8'}
   data = {
   "ApiKey":14257895,
   "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
   "ChannelId":0,
   "ProfileId":0,
   "CompanyId":0,
   "StatusIds":[1,2],
   "MeetingTypeIds":[1],
   "StartDate":str(today),
   "EndDate":str(today + one_year),
   "SearchTerm":"",
   "ShowNoInvoice":False,
   "ShowNoRevenue":True,
   "ShowAmountOpen":False,
   "ShowOptionCategory":-1,
   "Page":1,
   "ItemsPerPage":amount
   }
   r = requests.get(url, params=json.dumps(data), headers=headers)
   return r.json()
   

            

def loadpage(request):
   things = get_s2m_res(100)
   #and now save the reservation
   #problem!!! An instance has subdicts(), but this for thinks every { is a new dict. so it repeats unnesecarily.  
   for reservation in things:

      #cut loose date
      res_date_created_split = reservation.get("CreatedOn").split("T")
      res_date_split = reservation.get("StartTime").split("T")
      
      #now poor into model and save
      new_res, created = Reservation.objects.get_or_create(
      res_id=reservation.get("Id"),
      res_location_id=reservation.get("LocationId"),
      res_company=reservation.get("CompanyName"),
      res_user=reservation.get("ProfileName"),
      res_desc=reservation.get("ReservationName"),
      res_date_created=res_date_created_split[0],
      res_date=res_date_split[0],
      res_status=reservation.get("StatusId"),
      res_total_seats=reservation.get("TotalSeats"),
      res_status_sales=1
      )      
   # context = {}
   # template = 'load.html'   
   # return render(request, template, context)
   return redirect('/')





def listall(request):
   
   # when user changes a reservation status, process it now.
   item_to_update = [] 
   if request.method == 'POST' and 'res_id' in request.POST:
      item_to_update = Reservation.objects.get(res_id=request.POST['res_id'])
      form = UpdateForm(request.POST or None, instance=item_to_update)
      if form.is_valid():
         form.save()
         
   #when user changes a filter, process it now
   if request.method == 'POST' and 'filter_name' in request.POST:
      filter_to_update = Filteroption.objects.get(filter_name=request.POST['filter_name'])
      form = UpdateFilter(request.POST or None, instance=filter_to_update)
      if form.is_valid():
         form.save()
   #get the list of reservations from db
   filteroptions_on = Filteroption.objects.all().filter(filter_status=0)
   
   #get list of all reservations
   res_list = Reservation.objects.all()
   #now filter through it for every filter
   for filteroption in filteroptions_on:
      #pass all filters. if the filter is off, take all the instances out of the list 
      if filteroption.filter_name == 'res_status_attention':
         res_list = filter(filter_res_status_attention, res_list)
      if filteroption.filter_name == 'res_status_final':
         res_list = filter(filter_res_status_final, res_list)
      if filteroption.filter_name == 'res_status_sales_1':
         res_list = filter(filter_res_status_sales_1, res_list)
      if filteroption.filter_name == 'res_status_sales_2':
         res_list = filter(filter_res_status_sales_2, res_list)
      if filteroption.filter_name == 'res_status_sales_3':
         res_list = filter(filter_res_status_sales_3, res_list)
      if filteroption.filter_name == 'res_status_sales_4':
         res_list = filter(filter_res_status_sales_4, res_list)
      if filteroption.filter_name == 'res_status_sales_5':
         res_list = filter(filter_res_status_sales_5, res_list)
      if filteroption.filter_name == 'res_status_sales_6':
         res_list = filter(filter_res_status_sales_6, res_list)
      if filteroption.filter_name == 'res_status_sales_7':
         res_list = filter(filter_res_status_sales_7, res_list)
      if filteroption.filter_name == 'res_status_sales_8':
         res_list = filter(filter_res_status_sales_8, res_list)
      if filteroption.filter_name == 'res_status_sales_9':
         res_list = filter(filter_res_status_sales_9, res_list)

   #get the list of statuscodes from db
   status_list = Statuscode.objects.all()
   
   #get the list of filters from db
   filter_list = Filteroption.objects.all()
   
   #count items in list of reservations
   list_size = len(res_list)

   context = {'res_list': res_list, 'status_list': status_list, 'updated_item': item_to_update, 'filter_list': filter_list, 'list_size': list_size}
   template = 'listall.html'
   return render(request, template, context)   




def home(request):
   
   #we want to show:
   #Reservation x has not been processed
   #res x's last action (to next step in sales) was 1 day ago. 
   #remind me tomorrow button - never show me this one again (change status_sales to success)
   #send offer.. (change status_sales to offer sent)   
   #after action 'last_action_date' is today..


   #when a user clicks 'next', save the items's last change date as today
   if request.method == 'POST' and 'res_untouched' in request.POST:
      item_to_update = Reservation.objects.get(res_id=request.POST['res_id'])
      form = TouchedForm(request.POST or None, instance=item_to_update)
      if form.is_valid():
         form.save()
   
   # when user changes a reservation status, process it now.
   item_to_update = []
   #define today for last_action_taken var
   today = datetime.date.today()
   if request.method == 'POST' and 'res_status_sales' in request.POST:
      item_to_update = Reservation.objects.get(res_id=request.POST['res_id'])
      form = UpdateForm(request.POST or None, instance=item_to_update)
      if form.is_valid():
         form.save()         
   
   #get list of all reservations !! i just want the next one that isn't processed yet
   res_list = Reservation.objects.all()
   #filter away stuff we don't need
   res_list = filter(filter_res_status_sales_8, res_list) #success we don't need to show
   res_list = filter(filter_res_status_sales_9, res_list) #failed we don't need to show
   res_list = filter(filter_res_touchedtoday, res_list) #touched today we don't need to show
   reservation = []
   no_res = ''
   if res_list:
      reservation = res_list[1]
   else:
      no_res = True

   #get the list of statuscodes from db
   status_list = Statuscode.objects.all()
   
   context = {'reservation': reservation, 'status_list': status_list, 'updated_item': item_to_update, 'today':today, 'no_res': no_res}
   template = 'home.html'   
   return render(request, template, context)