#!/usr/bin/env python
from django.core.management.base import BaseCommand
from django.shortcuts import render, redirect
import json, requests, datetime, time
from reservation.models import *
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from datetime import date
from django.utils import timezone


class Command(BaseCommand):
    
    #UPDATE-API remove get_s2m_res
    def get_s2m_res(self, location_id): #you should only do this in background, or when user presses refresh, and then still in background with alert 'this might take a minute'. 
       #set datetime for future date set
       #!!!!WHEN going live, parse all data in rows. Uncomment below to do all.
        page = 1 #!!!!change to 1 after testen
        rowsleft = 100000 #must define but can't be zero:)
        results=[]
        userlocation = Userlocation.objects.all().filter(location_id=location_id)[:1]#need to do this to get userkey for approval of accessing reservations
        for location in userlocation:
            while rowsleft > 0:
                url = 'https://apiv2.seats2meet.com/api/reservation/location/%s' % location_id
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
                print page
                
                if rowsleft == 100000:
                    if r == []:
                        rowsleft = 0
                    
                    elif r != []:
                        for var in r[:1]:
                            rowsleft = var.get("MoreRows")
                        
                else:
                    rowsleft -= 1    
                print "Rows Left%s" % rowsleft
            return results
        
        
    def get_s2m_res_updated(self, location_id): #all reservations where CreatedOn and UpdatedOn >= today
        page = 1 #!!!!change to 1 after testen
        rowsleft = 100000 #must define but can't be zero:)
        results=[]
        userlocation = Userlocation.objects.all().filter(location_id=location_id)[:1]#need to do this to get userkey for approval of accessing reservations
        for location in userlocation:
            while rowsleft > 0:
                url = 'https://apiv2.seats2meet.com/api/reservation/location/%s' % location_id
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
                "ChangeDate":str(datetime.date.today()),
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
                print page
                
                if rowsleft == 100000:
                    if r == []:
                        rowsleft = 0
                    elif r != []:
                        for var in r[:1]:
                            rowsleft = var.get("MoreRows")      
                else:
                    rowsleft -= 1    
                print "Rows Left%s" % rowsleft
            return results
        
        
    
    #retrieve locationlist
    def handle(self, *args, **options):
        locationlist = Userlocation.objects.all()
        
        finallist = []
        for location in locationlist:
            finallist.append(location.location_id)
        
        finallist = list(set(finallist)) #this list was made to cancel out duplicates
        
        for location in finallist:
            
            print location
            #UPDATE-API uncomment next line, remove 2nd line
            #for res in self.get_s2m_res_updated(location):
            for res in self.get_s2m_res(location):
                #cut loose date
                res_date_created_split = res.get("CreatedOn").split("T")
                res_date_split = res.get("StartTime").split("T")
                #now poor into model and save
                   
                #now check if the reservation already exists
                try: #can we find it?
                    findres = Reservation.objects.get(res_id=res.get("Id"))
                      
                except: #didn't find it
                    if res.get('StatusId') == 2: #if status is final, go to sales_step 5 and note it in log
                        sales_status = '5'
                    else: #else, just make it a 1
                        sales_status = '1'
                    
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
        Refreshlog.objects.create(status="Success")
            
            
            
       
