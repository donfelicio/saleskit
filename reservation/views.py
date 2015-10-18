from django.shortcuts import render, redirect
from reservation.models import *
from reservation.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .search import *
from .s2m import *
from .dicts import *
from django.http import *
import time
from django.db import connection


def search(request):
   connection.close()
   query_string = ''
   found_entries = False
   if ('q' in request.POST) and request.POST['q'].strip():
       query_string = request.POST['q']
       
       entry_query = get_query(query_string, ['res_company', 'res_user', 'res_id'])
       
       return Reservation.objects.filter(entry_query).order_by('res_id')


#some filters for later views    
def filter_res_status_sales_8(element):
    return element.res_status_sales != '8'

def filter_res_status_sales_9(element):
    return element.res_status_sales != '9'
   
#the loading page that gets and updates all reservations from s2m
def loadpage(request):
   connection.close()
   
   #set DB userprofile res_updated to 'busy'
   instance = Userprofile.objects.get(user_name=request.user.username)
   #check if firstrun, res_update is set to no by default (when created for first time)
   if instance.res_updated == 'no':
      firstrun = 'yes'
   else:
      firstrun = 'no'
   instance.res_updated = 'busy'
   instance.save()

   #get reservations   
   things = get_s2m_res(request)
   
   for reservation in things:
      #cut loose date
      res_date_created_split = reservation.get("CreatedOn").split("T")
      res_date_split = reservation.get("StartTime").split("T")
      #now poor into model and save
      
      if firstrun == 'yes':
         #if the res with s2m is final, make the sales status a success
         if reservation.get("StatusId") == 2:
            sales_status = '8'
         else:
            pass
      
      #if the res with s2m is cancelled, make the sales status a failure
      if reservation.get("StatusId") == 3:
         sales_status = '9'
      else:
         pass
      
      if reservation.get("StatusId") == 1:
         sales_status = '1'
      else:
         pass
         
      #now check if the reservation already exists
      try: #can we find it?
         findres = Reservation.objects.get(res_id=reservation.get("Id"))
            
      except: #didn't find it
         new_res = Reservation.objects.create(
         res_id=reservation.get("Id"),
         res_location_id=reservation.get("LocationId"),
         res_company=reservation.get("CompanyName"),
         res_user=reservation.get("ProfileName"),
         res_desc=reservation.get("ReservationName"),
         res_date_created=res_date_created_split[0],
         res_date=res_date_split[0],
         res_status_sales=sales_status,
         res_status=reservation.get("StatusId"),
         res_total_seats=reservation.get("TotalSeats")
         )
      else: #found it
         findres.res_company=reservation.get("CompanyName")
         findres.res_user=reservation.get("ProfileName")
         findres.res_desc=reservation.get("ReservationName")
         findres.res_date=res_date_split[0]
         findres.res_status=reservation.get("StatusId")

         #if the res with s2m is updated to cancelled, make the sales status a failure
         if reservation.get("StatusId") == 3:
            findres.res_status_sales = '9'
            
         findres.res_total_seats=reservation.get("TotalSeats")
         findres.save()

   #set DB userprofile res_updated to 'done'
   instance = Userprofile.objects.get(user_name=request.user.username)
   instance.res_updated = 'done'
   instance.save()
   
   return redirect('/')



def listall(request):
   connection.close()
   
   #define for search purposes
   found_entries = False
   
   # when user changes a reservation status, process it now.
   item_to_update = [] 
   if request.method == 'POST' and 'res_id' in request.POST:
      item_to_update = Reservation.objects.get(res_id=request.POST['res_id'])
      form = UpdateForm(request.POST or None, instance=item_to_update)
      if form.is_valid():
         form.save()
         
   #if search is done   
   found_entries = search(request)
   
   #get list of all reservations
   res_list = Reservation.objects.all().filter(res_location_id=get_location_id(request))

   #get the list of statuscodes from db
   status_list = Statuscode.objects.all()
      
   #count items in list of reservations
   list_size = len(res_list)
   
   #paginate the results to 25 per page
   paginator = Paginator(res_list, 25) # Show 25 contacts per page
   page = request.GET.get('page')
   try:
       reservationlist = paginator.page(page)
   except PageNotAnInteger:
       # If page is not an integer, deliver first page.
       reservationlist = paginator.page(1)
   except EmptyPage:
       # If page is out of range (e.g. 9999), deliver last page of results.
       reservationlist = paginator.page(paginator.num_pages)

   context = {'res_list': res_list, 'reservationlist': reservationlist, 'status_list': status_list, 'updated_item': item_to_update, 'list_size': list_size,  'found_entries': found_entries}
   template = 'listall.html'
   return render(request, template, context)


def create_locationlist(request):
   connection.close()
   res_status = Userprofile.objects.get(user_name=request.user.username)
   
   if request.user.username and res_status.res_updated != 'busy' and res_status.res_updated != 'done' and res_status.res_updated != 'nope':
      print res_status.res_updated
      #set DB userprofile res_updated to 'busy'
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.res_updated = 'busy'
      instance.save()
    
      locationlist = s2m_locationlist() #get all locations to check if a user is allowed in list
      for location in locationlist:
         print location.get("Id")
         url = 'https://www.seats2meet.com/api/accounts/hasaccess/%s/%s' % (location.get("Id"), get_user_key(request))
         headers = {'content-type':'application/json'}
         data = {}
     
         r = requests.get(url, data=json.dumps(data), headers=headers)
         r = json.loads(r.text)
         if r:
             
          # if true, put it to the db.
            Userlocation.objects.get_or_create(location_id=location.get("Id"), user_key=get_user_key(request), location_name=location.get("Name"))
   
      #set DB userprofile res_updated to 'done'
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.res_updated = 'nope'
      instance.save()


def home(request):
   connection.close()
       
   today = datetime.date.today()
   one_day = datetime.timedelta(days=1)
   one_week = datetime.timedelta(weeks=1)
   one_month = datetime.timedelta(weeks=4)
   days_untouched = 0
   
   #load this if user is logged in and set some empty stuff for later if it isn't used
   no_res = True
   sales_tip = ''
   days_to_res = ''
   days_last_change = ''
   reservation = ''
   status_list = ''
   res_open = ''
   loading = ''
   filtered_res_list = ''
   
      
   #If user has selected a location when he has access to multiple, save the active_location now
   if request.method == 'POST' and 'location_id' in request.POST:
      
      #if needed create and always update active location and last login to today.
      instance, created = Userprofile.objects.get_or_create(user_name=request.user.username)
      instance.active_location=request.POST['location_id']
      instance.last_login=today
      instance.save()
      
      p = Process(target=loadpage, args=(request,), name='res_loader')
      p.start()
      

         
   
   if request.method == 'POST' and 'logout' in request.POST:
      return redirect('/logout')
      
   
   #when a user clicks 'next', save the items's last change date as today
   #define today for last_action_taken var
   
   if request.method == 'POST' and 'hide_days' in request.POST:
      form = HidereservationForm(request.POST or None)
      request.POST._mutable = True
      #now set the last_action_taken so the user will be reminded as asked (1 day is (Date.today), so it will show up tomorrow)
      if request.POST['hide_days'] == '1': #next or 1 day
         request.POST['hide_days'] = today
      elif request.POST['hide_days'] == '2': #2 days
         request.POST['hide_days'] = today + one_day
      elif request.POST['hide_days'] == '3': #3 days
         request.POST['hide_days'] = today + one_day + one_day
      elif request.POST['hide_days'] == '4': #4 days
         request.POST['hide_days'] = today + one_day + one_day + one_day
      elif request.POST['hide_days'] == '5': #5 days
         request.POST['hide_days'] = today + one_day + one_day + one_day + one_day
      elif request.POST['hide_days'] == '14': #14 days
         request.POST['hide_days'] = today + one_week + one_week
      elif request.POST['hide_days'] == '30': #30 days
         request.POST['hide_days'] = today + one_month
      if form.is_valid():
         form.save()
         
            
   # when user changes a reservation status, process it now.
   item_to_update = []
   if request.method == 'POST' and 'res_status_sales' in request.POST:
      item_to_update = Reservation.objects.get(res_id=request.POST['res_id'])
      form = UpdateForm(request.POST or None, instance=item_to_update)
      if form.is_valid():
         form.save()
   
   p = Process(target=create_locationlist, args=(request,), name='create_locationlist')
   p.start()
   connection.close()
   if request.user.username: #if user is logged in
      
      locationlist = Userlocation.objects.all().filter(user_key=get_user_key(request))

      time.sleep(1)
      check_if_loading = Userprofile.objects.get(user_name=request.user.username)
      if check_if_loading.active_location == '0':
         if check_if_loading.res_updated == 'busy':
            loading = 'still loading'
            context = {'loading': loading}
         else:
            loading = ''      
            context = {'locationlist': locationlist, 'loading': loading}
         template = 'select.html'   
         return render(request, template, context)

      
      #check if it's the same day as last_login, otherwise checkout
      check_if_sameday = Userprofile.objects.get(user_name=request.user.username)
      if check_if_sameday.last_login != today:
         return redirect('/logout')
         
      #get list of all reservations !! i just want the next one that isn't processed yet
      res_list = Reservation.objects.all().filter(res_location_id=get_location_id(request))
      #filter away stuff we don't need
      res_list = filter(filter_res_status_sales_8, res_list) #success we don't need to show
      res_list = filter(filter_res_status_sales_9, res_list) #failed we don't need to show
      reservation = []
      if res_list:
         filtered_res_list = []
         #get the first reservation that's not in the hidereservation table
         for reservation in res_list:
            try:
               matchtohide = Hidereservation.objects.get(res_id=reservation.res_id, user_name=request.user.username)
            except: #didn't find it
               no_res = False
               filtered_res_list.append(reservation)
            else: #found it
               pass
               
      if filtered_res_list != [] and filtered_res_list != '':
         res_open = len(filtered_res_list) #count amount of reservations to go
         
         reservation = filtered_res_list[0] #just need the next reservation:)
         
         #get how long ago it was changed      
         days_untouched = today - reservation.res_last_change_date
         days_untouched = getattr(days_untouched, "days")
         
         #now get the sales tip from dicts
         sales_tip = salestip(reservation.res_status_sales)
         
         #now get days until reservation
         days_to_res = reservation.res_date - today
         days_to_res = getattr(days_to_res, "days")
         
         #figure out when last change was done
         days_last_change = today - reservation.res_last_change_date
         days_last_change = getattr(days_last_change, "days")
      
         #get the list of statuscodes from db
         status_list = Statuscode.objects.all()
         
      check_if_loading = Userprofile.objects.get(user_name=request.user.username)
      if check_if_loading.res_updated == 'busy':
         loading = 'still loading'
      else:
         loading = ''
      
      context = {
         'reservation': reservation,
         'status_list': status_list,
         'updated_item': item_to_update,
         'today':today,
         'no_res': no_res,
         'days_untouched': days_untouched,
         'sales_tip': sales_tip,
         'res_open': res_open,
         'days_to_res': days_to_res,
         'days_last_change': days_last_change,
         'loading': loading
         }
      template = 'home.html'   
      return render(request, template, context)
   
   #if loggedout   
   context = {}
   template = 'home.html'   
   return render(request, template, context)

def help(request):
   context = {}
   template = 'help.html'   
   return render(request, template, context)

def logout(request):
   connection.close()
   instance = Userprofile.objects.get(user_name=request.user.username)
   instance.active_location = 0
   instance.res_updated = 'done'
   instance.save()
   s2m_logout(request)
   return redirect('/')

def login(request):
   connection.close()
   s2m_login(request)
   return redirect('/')