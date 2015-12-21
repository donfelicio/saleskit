from django.shortcuts import render, redirect
from reservation.models import *
from reservation.forms import *
from invoice.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .s2m import *
from .dicts import *
from django.http import *
import time, random
from django.db.models import Q
from threading import Thread


   
def filter_over20(element):
    return int(element.res_total_seats) >= 20
   
def filter_attention(element):
    return element.res_status == '1'
   
def filter_request_received(element):
    return element.res_status_sales == '1'
   


def loadpage_updated(request, refresh):
    
   #set DB userprofile res_updated to 'busy'
   instance = Userprofile.objects.get(user_name=request.user.username)
   instance.res_updated = 'busy'
   instance.save()
   
   #if some other user already added the location, we don't have to do this now. There's just 1 location if this hasn't happend
   #or if user clicks refresh
   if len(Userlocation.objects.all().filter(location_id=Userprofile.objects.get(user_name=request.user.username).active_location)) == 1 or request.GET.get('refresh', '') == 'yes':
      for res in get_s2m_res_updated(request, refresh):
         
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
               findres.res_status_sales='9'
               
            findres.res_total_seats=res.get("TotalSeats")
            findres.save()

   #set DB userprofile res_updated to 'done'
   instance = Userprofile.objects.get(user_name=request.user.username)
   instance.res_updated = 'done'
   instance.save()
   return redirect('/')



def create_locationlist(request, userprofile, locationlist):
   #set DB userprofile res_updated to 'busy'
   instance = Userprofile.objects.get(user_name=request.user.username)
   instance.loc_updated = 'busy'
   instance.save()
   
   #get all locations to check if a user is allowed in list
   for location in locationlist:
      if 1 in location.get('MeetingTypeIds'):
         print location.get('Id')
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
         res_list = Reservation.objects.filter(res_location_id=Userprofile.objects.get(user_name=request.user.username).active_location).exclude(res_status_sales=8).exclude(res_status_sales=9).filter(Q(res_user__icontains=request.POST['q']) | Q(res_company__icontains=request.POST['q']) | Q(res_id__icontains=request.POST['q']) | Q(res_desc__icontains=request.POST['q']))
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
   for resfilter in Reservationfilter.objects.all():
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
   notification = False
   
   # if there, show notification
   if request.GET.get('noty') == 'day':
      notification = "Saved, reservation hidden until tomorrow morning"
   elif request.GET.get('noty') == 'after':
      notification = "Saved, reservation hidden until day after meeting"
   elif request.GET.get('noty') == 'forever':
      notification = "Reservation removed from saleskit"
   elif request.GET.get('noty') == 'comment':
      notification = "Note added"
   elif request.GET.get('noty') == 'hour':
      notification = "Reservation hidden for one hour"
   elif request.GET.get('noty') == 'week':
      notification = "Reservation hidden for one week"
   elif request.GET.get('noty') == 'month':
      notification = "Reservation hidden for one month"
   elif request.GET.get('noty') == 'hidden':
      notification = "Reservation hidden from you forever"
   elif request.GET.get('noty') == 'select':
      notification = "Now hide the reservation for as long as you want"
   elif request.GET.get('noty') == 'selected':
      notification = "Reservation is now hidden until selected date"
   
   
   
   #is user clicked 'refresh', do the refresh.
   if request.GET.get('refresh', '') == 'yes' and Userprofile.objects.get(user_name=request.user.username).res_updated != 'busy':
      b = Thread(target=loadpage_updated, args=(request, True))
      b.daemon = True
      b.start()
      time.sleep(1)
      return redirect('/')
   
   #if user clicks 'change location', set active location to False
   if request.GET.get('loc_change', '') == 'yes' and Userprofile.objects.get(user_name=request.user.username).res_updated != 'busy':
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.active_location = False
      instance.save()
      return redirect('/')
      
   #If user has selected a location when he has access to multiple, save the active_location now
   if request.method == 'POST' and 'location_id' in request.POST:
      #if needed create userprofile and always update active location.
      instance, created = Userprofile.objects.get_or_create(user_name=request.user.username)
      instance.active_location=request.POST['location_id']
      instance.save()

      if Userprofile.objects.get(user_name=request.user.username).res_updated == 'no' or len(Reservation.objects.all().filter(res_location_id=request.POST['location_id'])) == 0:      
         b = Thread(target=loadpage_updated, args=(request, False)) 
         b.daemon = True
         b.start()
         time.sleep(1)
      return redirect('/')
   
   #if user assigned the reservation to someone
   if request.method == 'POST' and 'assign_to' in request.POST:
      instance = Reservation.objects.get(res_id=request.POST['res_id'])
      instance.res_assigned = request.POST['assign_to']
      instance.save()
   
   #if a specific reservation is selected from the list to edit, update DB to this res
   if request.GET.get('active_res'):
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.active_reservation = request.GET.get('active_res')
      instance.save()
   
   #when a user clicks 'next', save the items's last change date as today 
   if request.method == 'POST' and 'hide_days' in request.POST:
      if request.POST['hide_days'] != '':
      
         if request.POST['hide_days'] == "today":
            now_plus_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
            Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=(datetime.datetime.now()), hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))
         elif request.POST['hide_days'] == "tomorrow":
            now_plus_hour = datetime.datetime.strptime('00:00', '%H:%M')
            Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=(datetime.datetime.now() + datetime.timedelta(days=1)), hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))
         elif request.POST['hide_days'] == "month":
            now_plus_hour = datetime.datetime.strptime('00:00', '%H:%M')
            Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=(datetime.datetime.now() + datetime.timedelta(weeks=4)), hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))
         elif request.POST['hide_days'] == "week":
            now_plus_hour = datetime.datetime.strptime('00:00', '%H:%M')
            Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=(datetime.datetime.now() + datetime.timedelta(weeks=1)), hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))
         elif request.POST['method'] == "datepicker":
            now_plus_hour = datetime.datetime.strptime('00:00', '%H:%M')
            Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=request.POST['hide_days'], hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))
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
      if len(Userlocation.objects.all().filter(user_name=request.user.username)) == 0:
         p = Thread(target=create_locationlist, args=(request, Userprofile.objects.get(user_name=request.user.username),s2m_locationlist()))
         p.daemon = True
         p.start()
         time.sleep(5)
         #p.join()
         #create_locationlist(request, Userprofile.objects.get(user_name=request.user.username))

      #als geen actieve locatie, dan laten kiezen. Of kies auto als er maar 1 is
      if Userprofile.objects.get(user_name=request.user.username).active_location == 'False':
         if len(Userlocation.objects.all().filter(user_name=request.user.username)) == 1:
            instance, created = Userprofile.objects.get_or_create(user_name=request.user.username)
            instance.active_location=Userlocation.objects.get(user_name=request.user.username).location_id
            instance.save()
            
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

         res_list = Reservation.objects.all().filter(res_location_id=Userprofile.objects.get(user_name=request.user.username).active_location).exclude(reservationfilter__isnull=False, reservationfilter__user_name=request.user.username).exclude(reservationfilter__isnull=False, res_status_sales='6').exclude(res_status_sales='8').exclude(res_status_sales='9').filter(Q(res_assigned='no') | Q(res_assigned=request.user.username))
         
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
         'userprofile': Userprofile.objects.get(user_name=request.user.username),
         'locationlist': Userlocation.objects.all().filter(user_name=request.user.username),
         'notification': notification
         }
      
      if len(critical) > 0:
         context['critical'] = len(critical)
      if len(important) > 0:
         context['important'] = len(important)
         
      if no_res == False: #if there is a reservation then...
         context['reservation_s2m'] = get_s2m_res_single(request,reservation.res_id)
         context['reservation_s2m_revisions'] = get_s2m_res_single_revisions(request,reservation.res_id)
         context['location_profile_list'] = Userlocation.objects.all().filter(location_id=Userprofile.objects.get(user_name=request.user.username).active_location)
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





def status_change(request):
   notification = False
   #if change of sales status and note are added, save to db
   
   if request.method == 'POST' and 'res_id' in request.POST:
      
      #update the reservation
      instance = Reservation.objects.get(res_id=request.POST['res_id'])
      instance.res_prev_status=request.POST['res_prev_status']
      instance.res_last_change_by=request.POST['res_last_change_by']
      instance.res_status_sales=request.POST['res_status_sales']
      instance.save()
      
      #make sure the userprofile doesn't have an active reservation anymore that selects the res to edit
      instance = Userprofile.objects.get(user_name=request.user.username)
      instance.active_reservation = '0'
      instance.save()
      
      #if status_sales is 'prepared', hide until one day after the meeting.
      if request.POST['res_status_sales'] == '6':
         now_plus_hour = datetime.datetime.strptime('00:00', '%H:%M')
         Reservationfilter.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, location_id=Userprofile.objects.get(user_name=request.user.username).active_location, hide_days=(Reservation.objects.get(res_id=request.POST['res_id']).res_date + datetime.timedelta(days=1)), hide_hour=now_plus_hour.strftime('%H'), hide_minute=now_plus_hour.strftime('%M'))
         notification = 'after'
      elif request.POST['res_status_sales'] == '7':
         instance = Reservation.objects.get(res_id=request.POST['res_id'])
         instance.res_status_sales='8'
         instance.save()
         notification = 'forever'
      elif request.POST['res_status_sales'] == '8' or request.POST['res_status_sales'] == '9' or request.POST['res_status_sales'] == '10':
         notification = 'forever'
      elif request.POST['res_prev_status'] != request.POST['res_status_sales']:
      #or else hide the reservation until tomorrow
         notification = 'select'
      else:
         notification = 'comment'
      
      #add the statuschange instance
      instance = Statuschange.objects.create(reservation=Reservation.objects.get(res_id=request.POST['res_id']), user_name=request.user.username, res_status_sales_code=request.POST['res_status_sales'], res_status_sales=Statuscode.objects.get(status_code=request.POST['res_status_sales']).description_short, change_note=request.POST['change_note'])      
      if notification != False:
         url = "/?noty=%s" % notification
      else:
         url = "/"
      return redirect(url)




def add_lead(request):
   
   if request.method == 'POST':
      
      #error handling
      try: #check if total seats is a number
        int(request.POST['total_seats'])  
      except: #not
         total_seats = 0
      else: #yes
         total_seats = request.POST['total_seats']
         
      
      if request.POST['date'] != '':
         res_date_input = request.POST['date']
      else:
         res_date_input = datetime.date.today()
      
      #define current user full name   
      current_user = "%s %s" %(request.user.first_name, request.user.last_name)
      
      #add the reservation.
      Reservation.objects.create(res_id=random.randint(1000000000,9999999999), res_user=request.POST['profile'], res_company=request.POST['company'], res_desc=request.POST['description'], res_total_seats=total_seats, res_date=res_date_input, res_date_created=datetime.date.today(), res_location_id=Userprofile.objects.get(user_name=request.user.username).active_location, res_last_change_by=current_user, res_manual_added='yes')
      return redirect('/')
   
   context={}
   template="add_lead.html"
   return render(request, template, context)



def logout(request):
   instance = Userprofile.objects.get(user_name=request.user.username)
   instance.active_location = False
   instance.active_reservation = '0'
   instance.res_updated = 'done'
   instance.save()
   request.session.flush()
   return redirect('/')



def logs(request):
   context={
         'loginlog':Loginlog.objects.all()[:10],
         'refreshlog':Refreshlog.objects.all()[:1],
         'remindlog':Remindlog.objects.all()[:1],
         'invoicelog':Invoicereminder.objects.all()[:10],
        }
   template="logs.html"
   return render(request, template, context)
   



def login(request):
   s2m_login(request)
   #run the login processes (removal of old filters, reservations, etc..)
   return redirect('/')