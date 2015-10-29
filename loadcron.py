#!/usr/bin/env python
from django.shortcuts import render, redirect
import json, requests, datetime
from reservation.models import *


def get_s2m_res(location_id): #you should only do this in background, or when user presses refresh, and then still in background with alert 'this might take a minute'. 
   #set datetime for future date set
   #!!!!WHEN going live, parse all data in rows. Uncomment below to do all.
    page = 1 #!!!!change to 1 after testen
    rowsleft = 100000 #must define but can't be zero:)
    results=[]
    userlocation = Userlocation.objects.all().filter(location_id=location_id)[:1]#need to do this to get userkey for approval of accessing reservations
    for location in userlocation:
        
        while rowsleft > 0:
            url = 'http://www.seats2meet.com/api/reservation/location/%s' % location_id
            headers = {'content-type':'application/json', 'Connection':'close'}
            data = {
            "ApiKey":91216637,
            "ProfileKey":Userprofile.objects.get(user_name=location.user_name).user_key,
            "ChannelId":0,
            "ProfileId":0,
            "CompanyId":0,
            "StatusIds":[1,2,3],
            "MeetingTypeIds":[1],
            "StartDate":str(datetime.date.today()),
            "EndDate":str(datetime.date.today() + datetime.timedelta(weeks=52)),
            "SearchTerm":"",
            "ShowNoInvoice":False,
            "ShowNoRevenue":True,
            "ShowAmountOpen":False,
            "ShowOptionCategory":-1,
            "Page":page,
            "ItemsPerPage":50
            }
            
            r = requests.get(url, params=json.dumps(data), headers=headers)
            r = json.loads(r.text)
            results.extend(r)
            #up page 1
            page += 1
            
            if rowsleft == 100000:
                for var in r[:1]:
                    rowsleft = var.get("MoreRows")
            else:
                rowsleft -= 1
            print rowsleft      
            
            return results




#lijst met alle locaties ophalen
locationlist = Userlocation.objects.all()

finallist = []
for location in locationlist:
    finallist.append(location.location_id)

finallist = list(set(finallist)) #this list was made to cancel out duplicates

for location in finallist:
        
    for reservation in get_s2m_res(location):
        #cut loose date
        res_date_created_split = reservation.get("CreatedOn").split("T")
        res_date_split = reservation.get("StartTime").split("T")
        #now poor into model and save
           
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









