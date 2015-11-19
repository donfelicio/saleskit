from django.shortcuts import render, redirect
from reservation.models import *
from reservation.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .s2m import *
from .dicts import *
from django.http import *
import time
from django.db.models import Q
from threading import Thread

   
def filter_over20(element):
    return int(element.res_total_seats) >= 20
   
def filter_attention(element):
    return element.res_status == '1'
   
def filter_request_received(element):
    return element.res_status_sales == '1'
   

   
#the loading page that gets and updates all reservations from s2m
def loadpage(request):
    
   #set DB userprofile res_updated to 'busy'
   instance = Userprofile.objects.get(user_name=request.user.username)
   #check if firstrun, res_update is set to no by default (when created for first time)
   ran_before = instance.res_updated
   instance.res_updated = 'busy'
   instance.save()
   
   for res in get_s2m_res(request):
      #cut loose date
      res_date_created_split = res.get("CreatedOn").split("T")
      res_date_split = res.get("StartTime").split("T")
      #now poor into model and save
      
      #if the res with s2m is cancelled, make the sales status a failure
      if res.get("StatusId") == 3:
         sales_status = '9'
      elif res.get("StatusId") == 2:
         sales_status = '5' #if status is final, set to 'second call', and add to status change that this was made online, or was handled directly. 
      else: #status is 'attention required, so set it to the first sales status
         sales_status = '1'
         
      #now check if the reservation already exists
      try: #can we find it?
         findres = Reservation.objects.get(res_id=res.get("Id"))
            
      except: #didn't find it
         new_res = Reservation.objects.create(
         res_id=res.get("Id"),
         res_location_id=res.get("LocationId"),
         res_company=res.get("CompanyName"),
         res_user=res.get("ProfileName"),
         res_desc=res.get("ReservationName"),
         res_date_created=res_date_created_split[0],
         res_date=res_date_split[0],
         res_status_sales=sales_status,
         res_status=res.get("StatusId"),
         res_total_seats=res.get("TotalSeats")
         )
         if res.get("StatusId") == 2:
            #if status is final, set to 'second call', and add to status change that this was made online, or was handled directly. 
            instance = Statuschange.objects.get_or_create(reservation=Reservation.objects.get(res_id=res.get("Id")), user_name="system", res_status_sales_code='5', res_status_sales=Statuscode.objects.get(status_code='5').description_short, change_note="This reservation was created via the website, or it was finalized by your team")
      else: #found it
         findres.res_company=res.get("CompanyName")
         findres.res_user=res.get("ProfileName")
         findres.res_desc=res.get("ReservationName")
         findres.res_date=res_date_split[0]
         findres.res_status=res.get("StatusId")

         #if the res with s2m is updated to cancelled, make the sales status a failure
         if res.get("StatusId") == 3:
            findres.res_status_sales = '9'
            
         findres.res_total_seats=res.get("TotalSeats")
         findres.save()

   #set DB userprofile res_updated to 'done'
   instance = Userprofile.objects.get(user_name=request.user.username)
   instance.res_updated = 'done'
   instance.save()
   return redirect('/')



def create_locationlist(request, userprofile, locationlist):
   
   if userprofile.loc_updated != 'busy' and userprofile.loc_updated != 'done':
      #set DB userprofile res_updated to 'busy'
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.loc_updated = 'busy'
      instance.save()
      
      #get all locations to check if a user is allowed in list
      for location in locationlist:
         print location.get("Id")
         url = 'https://apiv2.seats2meet.com/api/accounts/hasaccess/%s/%s' % (location.get("Id"), userprofile.user_key)
         headers = {'content-type':'application/json'}
         data = {}
     
         r = requests.get(url, data=json.dumps(data), headers=headers)
         r = json.loads(r.text)
         if r:
          # if true, add to the list
            Userlocation.objects.get_or_create(location_id=location.get("Id"), user_name=userprofile.user_name, location_name=location.get("Name"))
   
      #set DB userprofile res_updated to 'done'
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.loc_updated = 'done'
      instance.save()
   
    
    
    
def listall(request):
   if request.user.username: #if user is logged in 
      if request.method == 'POST' and 'q' in request.POST:
         res_list = Reservation.objects.filter(res_location_id=Userprofile.objects.get(user_name=request.user.username).active_location).exclude(res_status_sales=8).exclude(res_status_sales=9).filter(Q(res_user__icontains=request.POST['q']) | Q(res_company__icontains=request.POST['q']) | Q(res_id__icontains=request.POST['q']))
      else:
         res_list = Reservation.objects.all().filter(res_location_id=Userprofile.objects.get(user_name=request.user.username).active_location).exclude(res_status_sales='8').exclude(res_status_sales='9')
      
      #now test for stage of critical, important or dontforget
      critical = filter(filter_over20, res_list)
      critical = filter(filter_attention, critical)
      critical = filter(filter_request_received, critical)
      
      important = filter(filter_attention, res_list)
      important = set(important) - set(critical)
      res_list = set(res_list) - set(important) - set(critical)
      
      
      context={
         'reservationlist':res_list,
        }
      if len(critical) > 0:
         context['critical'] = critical
      if len(important) > 0:
         context['important'] = important
         
      template="listall.html"
      return render(request, template, context)
   else:
      return redirect ('/')

      

def home(request):
   
   #delete all the users old hidereservation instances (older than today)
   for resfilter in Reservationfilter.objects.all().filter(user_name=request.user.username):
      if resfilter.hide_days < datetime.date.today():
         resfilter.delete()
      elif resfilter.hide_days == datetime.date.today() and (int(resfilter.hide_hour) - int(datetime.datetime.now().time().strftime('%H'))) * 60 + (int(resfilter.hide_minute) - int(datetime.datetime.now().time().strftime('%M'))) < 0:
         resfilter.delete()

   
   #load this if user is logged in and set some empty stuff for later if it isn't used
   no_res = True
   sales_tip = ''
   days_to_res = ''
   days_last_change = ''
   reservation = ''
   status_list = ''
   res_open = ''
   loading = ''
   critical = []
   important = []
   res_list = []
   
   
   #is user clicked 'refresh', do the refresh.
   if request.GET.get('refresh', '') == 'yes' and Userprofile.objects.get(user_name=request.user.username).res_updated != 'busy':
      b = Thread(target=loadpage, args=(request,)) 
      b.daemon = True
      b.start()
      time.sleep(1)
      return redirect('/')
   
      
   #If user has selected a location when he has access to multiple, save the active_location now
   if request.method == 'POST' and 'location_id' in request.POST:
      
      #if needed create and always update active location.
      instance, created = Userprofile.objects.get_or_create(user_name=request.user.username)
      instance.active_location=request.POST['location_id']
      instance.save()

      if Userprofile.objects.get(user_name=request.user.username).res_updated == 'no':      
         b = Thread(target=loadpage, args=(request,)) 
         b.daemon = True
         b.start()
         time.sleep(1)
      return redirect('/')
   
   #if a specific reservation is selected from the list to edit, update DB to this res
   if request.GET.get('active_res'):
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.active_reservation = request.GET.get('active_res')
      instance.save()
   
   #when a user clicks 'next', save the items's last change date as today 
   if request.method == 'POST' and 'hide_days' in request.POST:
      if request.POST['hide_days'] != '':
         
         # #old version with datepicker
         # if datetime.datetime.strptime(request.POST['hide_days'], '%m/%d/%Y').strftime('%Y-%m-%d') == str(datetime.date.today()):
         #    now_plus_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
         # else:
         #    now_plus_hour = datetime.datetime.strptime('00:00', '%H:%M')
         if request.POST['hide_days'] == "today":
            now_plus_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
            Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=(datetime.datetime.now()), hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))
         elif request.POST['hide_days'] == "forever":
            now_plus_hour = datetime.datetime.strptime('00:00', '%H:%M')
            Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=(datetime.datetime.now() + datetime.timedelta(days=999999)), hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))
         elif request.POST['hide_days'] == "month":
            now_plus_hour = datetime.datetime.strptime('00:00', '%H:%M')
            Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=(datetime.datetime.now() + datetime.timedelta(weeks=4)), hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))
         else: #tomorrow
            now_plus_hour = datetime.datetime.strptime('00:00', '%H:%M')
            Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=(datetime.datetime.now() + datetime.timedelta(days=1)), hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))
   #make sure the userprofile doesn't have an active reservation anymore that selects the res to edit
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.active_reservation = '0'
      instance.save()
      
   #if someone cancels the 'now editing active_reservation' mode
   if request.GET.get('no_active_res'):
      #make sure the userprofile doesn't have an active reservation anymore that selects the res to edit
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.active_reservation = '0'
      instance.save()
   
   if request.user.username: #if user is logged in            
      #check if it's the same day as last_login, otherwise checkout
      if Userprofile.objects.get(user_name=request.user.username).last_login != datetime.date.today():
         return redirect('/logout')
      
      #maak nu de locationlist terwijl de gebruiker wacht, firstrun only
      if Userprofile.objects.get(user_name=request.user.username).loc_updated == 'no':
         p = Thread(target=create_locationlist, args=(request, Userprofile.objects.get(user_name=request.user.username),s2m_locationlist()))
         p.daemon = True
         p.start()
         time.sleep(1)
         #p.join()
         #create_locationlist(request, Userprofile.objects.get(user_name=request.user.username))

      #als geen actieve locatie, dan laten kiezen
      if Userprofile.objects.get(user_name=request.user.username).active_location == 'False':
         context = {
            'locationlist': Userlocation.objects.all().filter(user_name=request.user.username),
            'userprofile': Userprofile.objects.get(user_name=request.user.username)
                    }
         template = 'select.html'
         return render(request, template, context)


         

      #get list of all reservations !! i just want the next one that isn't processed yet
      active_reservation_id = Userprofile.objects.get(user_name=request.user.username).active_reservation
      if active_reservation_id != '0': #deze uit DB gaan halen, niet uit url 
         reservation = Reservation.objects.get(res_id=active_reservation_id)
         no_res = False
      else:
         #make res list, filter out any reservations that have a filter from this user, and are final or success
         res_list = Reservation.objects.all().filter(res_location_id=Userprofile.objects.get(user_name=request.user.username).active_location).exclude(reservationfilter__isnull=False).exclude(res_status_sales='8').exclude(res_status_sales='9')
         
         #now test for stage of critical, important or dontforget
         critical = filter(filter_over20, res_list)
         critical = filter(filter_attention, critical)
         critical = filter(filter_request_received, critical)
         important = filter(filter_attention, res_list)
         
         
         if len(critical) > 0:
            reservation = critical[0]
            no_res = False
         elif len(important) > 0:
            reservation = important[0]
            no_res = False
         elif len(res_list) > 0: #if critical is empty, make important list
            reservation = res_list[0]
            no_res = False
         else:
            reservation = ''
      
      context = {
         'reservation': reservation,
         'status_list': Statuscode.objects.all(),
         'no_res': no_res,
         'userprofile': Userprofile.objects.get(user_name=request.user.username)
         }
      
      if len(critical) > 0:
         context['critical'] = len(critical)
      if len(important) > 0:
         context['important'] = len(important)
         
      if no_res == False: #if there is a reservation.. (might be empty list?)   
         context['status_changes'] = Statuschange.objects.all().filter(reservation=reservation)
         context['sales_tip'] = salestip(reservation.res_status_sales)
         context['short_sales_tip'] = short_salestip(reservation.res_status_sales)
         context['days_untouched'] = getattr(datetime.date.today() - reservation.res_last_change_date, "days")
         context['days_to_res'] = getattr(reservation.res_date - datetime.date.today(), "days")
      
      if Userprofile.objects.get(user_name=request.user.username).active_reservation == '0':
         context['res_open'] = len(res_list)
      
      if Userprofile.objects.get(user_name=request.user.username).active_reservation != '0':
         context['active_res'] = True
         
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





def res_input(request):
   #Let user add input to offer site
   if request.method == 'POST' and 'res_id' in request.POST:
      
      #update the reservation.
      instance = Reservation.objects.get(res_id=request.POST['res_id'])
      instance.res_intro=request.POST['res_intro']
      instance.save()
      return redirect('/')
   
   context={
      'res_id':request.GET.get('res_id', ''),
      'res_intro':Reservation.objects.get(res_id=request.GET.get('res_id', '')).res_intro
     }
   template="res_input.html"
   return render(request, template, context)




def status_change(request):
   #if change of sales status and note are added, save to db
   if request.method == 'POST' and 'res_id' in request.POST:
      
      #update the reservation
      instance = Reservation.objects.get(res_id=request.POST['res_id'])
      instance.res_prev_status=request.GET.get('res_prev_status')
      instance.res_last_change_by=request.GET.get('res_last_change_by')
      instance.res_status_sales=request.GET.get('res_status_sales')
      instance.save()
      
      #make sure the userprofile doesn't have an active reservation anymore that selects the res to edit
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.active_reservation = '0'
      instance.save()
      
      #if status_sales is 'prepared', hide until one day after the meeting.
      if request.GET.get('res_status_sales') == '6':
         now_plus_hour = datetime.datetime.strptime('00:00', '%H:%M')
         Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=(Reservation.objects.get(res_id=request.POST['res_id']).res_date + datetime.timedelta(days=1)), hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))

      else:
      #or else hide the reservation until tomorrow
         now_plus_hour = datetime.datetime.strptime('00:00', '%H:%M')
         Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=(datetime.datetime.now() + datetime.timedelta(days=1)), hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))
      
      #add the statuschange instance
      instance = Statuschange.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, res_status_sales_code=request.POST['res_status_sales'], res_status_sales=Statuscode.objects.get(status_code=request.GET.get('res_status_sales', '')).description_short, change_note=request.POST['change_note'])      
      return redirect('/')
   
   elif request.GET.get('res_status_sales') == '8' or request.GET.get('res_status_sales') == '9':
      #update the reservation
      instance = Reservation.objects.get(res_id=request.GET.get('res_id'))
      instance.res_prev_status=request.GET.get('res_prev_status')
      instance.res_last_change_by=request.GET.get('res_last_change_by')
      instance.res_status_sales=request.GET.get('res_status_sales')
      instance.save()
      
      #make sure the userprofile doesn't have an active reservation anymore that selects the res to edit
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.active_reservation = '0'
      instance.save()
      
      #add the statuschange instance
      instance = Statuschange.objects.create(reservation=Reservation.objects.get(res_id=request.GET.get('res_id')), user_name=request.user.username, res_status_sales_code=request.GET.get('res_status_sales'), res_status_sales=Statuscode.objects.get(status_code=request.GET.get('res_status_sales', '')).description_short, change_note="final change - by system")      
      return redirect('/')
      
   else:
      context={
         'res_id':request.GET.get('res_id', ''),
         'res_prev_status':request.GET.get('res_prev_status', ''),
         'res_last_changed_by':request.GET.get('res_last_changed_by', ''),
         'res_status_sales_code':request.GET.get('res_status_sales'),
         'res_status_sales':Statuscode.objects.get(status_code=request.GET.get('res_status_sales', '')).description_short,
        }
      template="status_change.html"
      return render(request, template, context)




def logout(request):
   instance = Userprofile.objects.get(user_name=request.user.username)
   instance.active_location = False
   instance.active_reservation = '0'
   instance.res_updated = 'done'
   instance.save()
   request.session.flush()
   return redirect('/')




def login(request):
   s2m_login(request)
   #run the login processes (removal of old filters, reservations, etc..)
   return redirect('/')