from django.core.management.base import BaseCommand
from django.shortcuts import render
import time, datetime, json, requests
from datetime import date
from django.shortcuts import redirect, render
from reservation.models import *
from invoice.models import *
from django.core.mail import send_mail


#TODO waar ben je?
#maak het een management/commands en dan schedule zonder render output
class Command(BaseCommand):
    
    def s2m_get_invoicelist(self):
    #NB: rowsleft doesn't work here, API doesn't show rows but a count of all items. 
        page = 1
        items = 20
        itemsleft = 100000
        results=[]
        while itemsleft > -20:
            url = 'https://apiv2.seats2meet.com/api/invoices/location/563'
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
                            
        return results
    
        
    #s2m API for sending an invoice
    def s2m_send_invoice(self, invoiceid, fromemail, toemail, subject, mailtext, invoice_code, LocationId):
        url = 'https://www.seats2meet.com/api/invoices/sendmail'
        headers = {'content-type':'application/json; charset-utf-8'}
        data = {
        "ApiKey":91216637,
        "ProfileKey": "6DE79403-D5EF-186C-9529-25ED04A66FD6",
        #"ProfileKey":Userprofile.objects.get(user_name=request.user.username).user_key,
        "InvoiceId": invoiceid,
        "ChannelId": 0,
        "FromEmail": fromemail,
        "ToEmail": toemail,
        "Cc":"",
        "Subject": subject,
        "MailText": mailtext,
        "Attachement": "Invoice",
        "IncludeComments": False,
        "LocationId": LocationId,
        }

        r = requests.post(url, data=json.dumps(data), headers=headers)
        print r
        return r

    

    
    #get directions to location
    #not being used right now, perhaps when making this multi-location
    def get_s2m_address(self, location):
        url = 'http://apiv2.seats2meet.com/api/locations/%s' % location
        headers = {'content-type':'application/json'}
        data = {
        "ApiKey":91216637,
        "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
        "locationId": location,
        }
        r = requests.get(url, params=json.dumps(data), headers=headers)
        r = json.loads(r.text)
        return r
    
    
    

    
    
    def handle(self, *args, **options):
        
        #location = self.get_s2m_address(invoice.get('LocationId'))
        location_name = 'Meet Berlage - S2M'
        location_admin_mail = 'info@meetberlage.com'
        location_id = 563
        test_mode = 'no'
        
        for item in self.s2m_get_invoicelist():
            # do NOT send to tax exempt people where the system thinks their tax still needs to be paid
            taxes = item.get('TotalIncludingTax') - item.get('TotalExcludingTax')
            if item.get('NoTax') == True and round(taxes,0) == round(item.get('AmountOpen'),0):
                pass
            elif item.get('AmountOpen') < 1.00: #als minder dan 1 euro openstaat.
                pass 
            else:#send them a fucking email
                two_weeks_after = datetime.datetime.strptime(str(item.get("ExpirationDate").split("T")[0]), '%Y-%m-%d')
                four_weeks_after = datetime.datetime.strptime(str(item.get("ExpirationDate").split("T")[0]), '%Y-%m-%d') + datetime.timedelta(weeks=2)
                six_weeks_after = datetime.datetime.strptime(str(item.get("ExpirationDate").split("T")[0]), '%Y-%m-%d') + datetime.timedelta(weeks=4)
                eight_weeks_after = datetime.datetime.strptime(str(item.get("ExpirationDate").split("T")[0]), '%Y-%m-%d') + datetime.timedelta(weeks=6)
                
                instance, created = Invoicereminder.objects.get_or_create(invoice_id=item.get('Id'))        
                invoice_reminder = Invoicereminder.objects.get(invoice_id=item.get('Id')).invoice_status    
                
                ####
                #####send 1st reminder
                ####
                if datetime.datetime.today() > two_weeks_after and datetime.datetime.today() < four_weeks_after and invoice_reminder != 1:
                    print 'stuur deze 1e %s' % item.get('Code')
                    subject = '%s invoice %s - first reminder' % (location_name, item.get('Code'))
                    mailtext = 'Dear %s </br></br>  This is the first reminder regarding payment of the attached invoice. </br>We kindly ask you to complete payment of the invoice directly, and to inform us about the payment by replying to this email. </br></br> Kind regards, </br> The %s Team' % (item.get('SendToName'), location_name)
                    
                    if test_mode != 'yes':
                        try:
                            self.s2m_send_invoice(item.get('Id'), location_admin_mail, item.get('EmailTo'), subject, mailtext, item.get('Code'), location_id)
                        except: #not, inform admin
                            print 'niet gelukt'
                            #email admin about failure
                            send_mail('Failed to send reminder for invoice %s' % item.get('Code'), 'Wasnt able to send the reminder for the invoice. perhaps the email address is missing in the account? Please send manually.', 'felix@donfelicio.com',[location_admin_email], fail_silently=False)
                        else: #done
                            print 'gelukt'
                            
                    ####then update database two_weeks instance to yes.
                        instance.invoice_status = 1
                        instance.save()
                
                ####
                #####send 2nd reminder
                ####
                if datetime.datetime.today() >= four_weeks_after and datetime.datetime.today() <= six_weeks_after and invoice_reminder != 2:
                    print 'stuur deze 2e %s' % item.get('Code')
                    subject = '%s invoice %s - second reminder' % (location_name, item.get('Code'))
                    mailtext = 'Dear %s </br></br>  This is the second reminder regarding payment of the attached invoice. </br>We kindly ask you to complete payment of the invoice directly, and to inform us about the payment by replying to this email. </br></br> Kind regards, </br> The %s Team' % (item.get('SendToName'), location_name)
                    
                    if test_mode != 'yes':
                        try:
                            self.s2m_send_invoice(item.get('Id'), location_admin_mail, item.get('EmailTo'), subject, mailtext, item.get('Code'), location_id)
                        except: #not, inform admin
                            print 'niet gelukt'
                            #email admin about failure
                            send_mail('Failed to send reminder for invoice %s' % item.get('Code'), 'Wasnt able to send the reminder for the invoice. perhaps the email address is missing in the account? Please send manually.', 'felix@donfelicio.com', [location_admin_email], fail_silently=False)
                        else: #done
                            print 'gelukt'
                    #then update database two_weeks instance to yes.
                        instance.invoice_status = 2
                        instance.save()
                
                ####
                #send 3rd reminder en naar infomail
                ####
                if datetime.datetime.today() >= six_weeks_after and datetime.datetime.today() <= eight_weeks_after and invoice_reminder != 3:
                    print 'stuur deze 3e %s' % item.get('Code')
                    subject = 'PLEASE NOTE: %s invoice %s - third reminder' % (location_name, item.get('Code'))
                    mailtext = 'Dear %s </br></br>  This is the third reminder regarding payment of the attached invoice. </br>We kindly ask you to complete payment of the invoice directly, and to inform us about the payment by replying to this email. </br></br> Kind regards, </br> The %s Team' % (item.get('SendToName'), location_name)

                    if test_mode != 'yes':                        
                        try:
                            self.s2m_send_invoice(item.get('Id'), location_admin_mail, item.get('EmailTo'), subject, mailtext, item.get('Code'), location_id)
                            send_mail('Just sent third reminder for invoice %s' % item.get('Code'), 'Perhaps its time to call your customer, they should really pay their invoice.', 'felix@donfelicio.com',[location_admin_email], fail_silently=False)
                        except: #not, inform admin
                            print 'niet gelukt'
                            #email admin about failure
                            send_mail('Failed to send reminder for invoice %s' % item.get('Code'), 'Wasnt able to send the reminder for the invoice. perhaps the email address is missing in the account? Please send manually.', 'felix@donfelicio.com', [location_admin_email], fail_silently=False)
                        else: #done
                            print 'gelukt'
                    #then update database two_weeks instance to yes.
                        instance.invoice_status = 3
                        instance.save()
                    
                ####
                #send last notice en naar infomail
                ####
                if datetime.datetime.today() >= eight_weeks_after and invoice_reminder != 4:
                    print 'stuur deze 4e %s' % (item.get('Code'))
                    subject = 'WARNING: %s invoice %s - fourth reminder' % (location_name, item.get('Code'))
                    mailtext = 'Dear %s </br></br>  This is the FOURTH AND FINAL REMINDER regarding payment of the attached invoice. </br>We kindly ask you to complete payment of the invoice directly, and to inform us about the payment by replying to this email. </br></br> Kind regards, </br> The %s Team' % (item.get('SendToName'), location_name)

                    if test_mode != 'yes':
                        try:
                            self.s2m_send_invoice(item.get('Id'), location_admin_mail, item.get('EmailTo'), subject, mailtext, item.get('Code'), location_id)
                            send_mail('Just sent FOURTH and final reminder for invoice %s' % item.get('Code'), 'Please call your customer, they should pay the invoice today!', 'felix@donfelicio.com',[location_admin_email], fail_silently=False)
                        except: #not, inform admin
                            print 'niet gelukt'
                            #email admin about failure
                            send_mail('Failed to send reminder for invoice %s' % item.get('Code'), 'Wasnt able to send the reminder for the invoice. perhaps the email address is missing in the account? Please send manually.', 'felix@donfelicio.com', [location_admin_email], fail_silently=False)
                        else: #done
                            print 'gelukt'
                    #then update database two_weeks instance to yes.
                        instance.invoice_status = 4
                        instance.save()       


