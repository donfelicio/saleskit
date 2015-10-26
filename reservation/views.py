from django.shortcuts import render, redirect
from reservation.models import *
from reservation.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .s2m import *
from .dicts import *
from django.http import *
import time
from django.db import connection


#some filters for later views    
def filter_res_status_sales_8(element):
    return element.res_status_sales != '8'

def filter_res_status_sales_9(element):
    return element.res_status_sales != '9'
   
   
#the loading page that gets and updates all reservations from s2m
def loadpage(request):
   
   #set DB userprofile res_updated to 'busy'
   instance = Userprofile.objects.get(user_name=request.user.username)
   #check if firstrun, res_update is set to no by default (when created for first time)
   ran_before = instance.res_updated
   instance.res_updated = 'busy'
   instance.save()
   
   
   for reservation in get_s2m_res(request):
      #cut loose date
      res_date_created_split = reservation.get("CreatedOn").split("T")
      res_date_split = reservation.get("StartTime").split("T")
      #now poor into model and save
      
      sales_status = '1'
      #HIER! firstrun werkt niet
      if ran_before == 'no':
         
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
   connection.close()
   return redirect('/')





def create_locationlist(request):
   connection.close()
   res_status = Userprofile.objects.get(user_name=request.user.username)
   
   if res_status.loc_updated != 'busy' and res_status.loc_updated != 'done':
      #set DB userprofile res_updated to 'busy'
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.loc_updated = 'busy'
      instance.save()
    
      locationlist = s2m_locationlist() #get all locations to check if a user is allowed in list
      for location in locationlist:
         print location.get("Id")
         url = 'https://www.seats2meet.com/api/accounts/hasaccess/%s/%s' % (location.get("Id"), Userprofile.objects.get(user_name=request.user.username).user_key)
         headers = {'content-type':'application/json'}
         data = {}
     
         r = requests.get(url, data=json.dumps(data), headers=headers)
         r = json.loads(r.text)
         if r:
             
          # if true, put it to the db.
            Userlocation.objects.get_or_create(location_id=location.get("Id"), user_name=request.user.username, location_name=location.get("Name"))
   
      #set DB userprofile res_updated to 'done'
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.loc_updated = 'done'
      instance.save()
      connection.close()


def home(request):
   connection.close()
   
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
      
      #if needed create and always update active location.
      instance, created = Userprofile.objects.get_or_create(user_name=request.user.username)
      instance.active_location=request.POST['location_id']
      instance.save()
      
      p = Process(target=loadpage, args=(request,), name='res_loader')
      p.start()
      
      
   
   #when a user clicks 'next', save the items's last change date as today 
   if request.method == 'POST' and 'hide_days' in request.POST:
      form = ReservationfilterForm(request.POST or None)
      request.POST._mutable = True
      request.POST['hide_days'] = datetime.date.today() + datetime.timedelta(days=int(request.POST['hide_days']))
      if form.is_valid():
         form.save()
         
            
   # when user changes a reservation status, process it now.
   item_to_update = []
   if request.method == 'POST' and 'res_status_sales' in request.POST:
      item_to_update = Reservation.objects.get(res_id=request.POST['res_id'])
      form = UpdateForm(request.POST or None, instance=item_to_update)
      if form.is_valid():
         form.save()
   
   
  
   if request.user.username: #if user is logged in
            
      #check if it's the same day as last_login, otherwise checkout
      if Userprofile.objects.get(user_name=request.user.username).last_login != datetime.date.today():
         return redirect('/logout')
      
      #maak nu de locationlist terwijl de gebruiker wacht
      if Userprofile.objects.get(user_name=request.user.username).loc_updated == 'no':
         p = Process(target=create_locationlist, args=(request,), name='create_locationlist')
         p.start()
         time.sleep(1)
      #als geen actieve locatie, dan laten kiezen
      if Userprofile.objects.get(user_name=request.user.username).active_location == 'False':
         context = {
            'locationlist': Userlocation.objects.all().filter(user_name=request.user.username),
            'userprofile': Userprofile.objects.get(user_name=request.user.username)
                    }
         template = 'select.html'
         connection.close()
         return render(request, template, context)


         
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
               Reservationfilter.objects.get(res_id=reservation.res_id, user_name=request.user.username)
            except: #No 'hide this res' filter was found
               no_res = False
               break
            else: #a 'hide this res' filter was found
               pass
      
      context = {
         'reservation': reservation,
         'status_list': Statuscode.objects.all(),
         'no_res': no_res,         
         'userprofile': Userprofile.objects.get(user_name=request.user.username)
         }
      
      if reservation: #if there is a reservation.. (might be empty list?)
         
         context['res_open'] = len(res_list) - len(Reservationfilter.objects.all().filter(user_name=request.user.username))
         context['sales_tip'] = salestip(reservation.res_status_sales)
         context['days_untouched'] = getattr(datetime.date.today() - reservation.res_last_change_date, "days")
         context['days_last_change'] = getattr(datetime.date.today() - reservation.res_last_change_date, "days")
         context['days_to_res'] = getattr(reservation.res_date - datetime.date.today(), "days")
         
      
      
      template = 'home.html'
      connection.close()
      return render(request, template, context)
   
   #if loggedout   
   context = {}
   template = 'home.html'
   connection.close()
   return render(request, template, context)

def help(request):
   context = {}
   template = 'help.html'   
   return render(request, template, context)

def logout(request):
   instance = Userprofile.objects.get(user_name=request.user.username)
   instance.active_location = False
   instance.res_updated = 'done'
   instance.save()
   request.session.flush()
   connection.close()
   return redirect('/')

def login(request):
   connection.close()
   s2m_login(request)
   connection.close()
   return redirect('/')