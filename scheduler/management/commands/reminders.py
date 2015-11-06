from django.core.management.base import BaseCommand
from django.shortcuts import render
import time, datetime, json, requests
from datetime import date
from django.shortcuts import redirect, render
from reservation.models import *
from invoice.models import *
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

#start pdf creation imports
import cStringIO as StringIO 
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape #end pdf creation imports


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
                        
        return results
    
    
    
    
    
    ###VERSIE 1 MET DE S2M SENDINVOICE API, ALS DIE WERKT
    
    
    # def s2m_send_invoice(request):
    #     url = 'http://www.seats2meet.com/api/invoices/sendmail'
    #     headers = {'content-type':'application/json', 'Connection':'close'}
    #     data = {
    #     "ApiKey":91216637,
    #     "ProfileKey": "6DE79403-D5EF-186C-9529-25ED04A66FD6",
    #    #"ProfileKey":Userprofile.objects.get(user_name=request.user.username).user_key,
    #     "InvoiceId": 112719,
    #     "ChannelId": 0,
    #     "FromEmail": "felix@meetberlage.com",
    #     "ToEmail": "felix@donfelicio.com",
    #     "Cc":"",
    #     "Subject": "test: invoices",
    #     "MailText": "test: invoice tekst",
    #     "Attachement": "",
    #     "IncludeComments": False,
    #     "LocationId": 563,
    #     }
    #   
    #     r = requests.post(url, data=json.dumps(data), headers=headers)
    #     print r
    #     return r
    #     
    # 
    # 
    # 
    # 
    # 
    # 
    # 
    
    
    
    
    
    
    
    
    
    ###VERSIE 2 ZONDER DE S2M SENDINVOICE API, ALS DIE DUS NIET WERKT
    
    
    
    def escape(self, html):
        """Returns the given HTML with ampersands, quotes and carets encoded."""
        return html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace("&#39;", '\'')
    
    
    
    
    def s2m_get_invoice(self, invoice_id):
        url = 'http://www.seats2meet.com/api/invoices/%s' % invoice_id
        headers = {'content-type':'application/json', 'Connection':'close'}
        data = {
        "ApiKey":91216637,
        "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
        "LocationId":"563",
        }
        r = requests.get(url, params=json.dumps(data), headers=headers)
        r = json.loads(r.text) 
        return r
    
    
    
    
    #get directions to location
    def get_s2m_address(self, location):
        url = 'http://www.seats2meet.com/api/locations/%s' % location
        headers = {'content-type':'application/json'}
        data = {
        "ApiKey":91216637,
        "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
        "locationId": location,
        }
        r = requests.get(url, params=json.dumps(data), headers=headers)
        r = json.loads(r.text)
        return r
    
    
    
    
    def render_to_pdf(self, template_src, context_dict):
        template = get_template(template_src)
        context = Context(context_dict)
        html  = template.render(context)
        result = StringIO.StringIO()
    
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return result
        else:
            return None
    
    
            
            
    def show_invoice(self, invoice_id):
    
        invoice = self.s2m_get_invoice(invoice_id)
    
        #calculate subtotals
        firstsub = 0
        secondsub = 0
        sixperc = 0
        twentyoneperc = 0
        for item in invoice.get('InvoiceLines'):
            if item.get('TextGroupId') == 1:
                firstsub += item.get('TotalPriceExcludingTax')
            elif item.get('TextGroupId') == 2:
                secondsub += item.get('TotalPriceExcludingTax')
        #now get tax amounts
            elif item.get('TextGroupId') == 5 and item.get('TaxId') == 3:
                sixperc += item.get('TotalPriceExcludingTax') * 0.06
            elif item.get('TextGroupId') == 5 and item.get('TaxId') == 6:
                twentyoneperc += item.get('TotalPriceExcludingTax') * 0.21
        context = {
            'invoice': invoice,
            'location': self.get_s2m_address(invoice.get('LocationId')),
            'footer': self.escape(invoice.get('Footer').replace('\"','')),
            'activation_date': datetime.datetime.strptime(str(invoice.get('ActivationDate').split("T")[0]), '%Y-%m-%d').strftime('%d-%b-%Y'),
            'expiration_date': datetime.datetime.strptime(str(invoice.get('ExpirationDate').split("T")[0]), '%Y-%m-%d').strftime('%d-%b-%Y'),
            'reservation_date': datetime.datetime.strptime(str(invoice.get('InvoiceReferences')[0].get('ReservationDate').split("T")[0]), '%Y-%m-%d').strftime('%d-%b-%Y'),
            'first_sub': firstsub,
            'second_sub': secondsub,
            'sixperc': sixperc,
            'twentyoneperc': twentyoneperc,
            }
        template = 'invoice.html'
        return self.render_to_pdf(template, context)
    
    
    
    
    
    def email_to_send(self, status, item):
        print 'email: %s -' % item.get('EmailTo')
        location_name = 'Meet Berlage - S2M'
        location_admin_mail = 'info@meetberlage.com'
        
        if status == 1:
            subject, from_email, to = '%s invoice %s - first reminder' % (location_name, item.get('Code')), location_admin_mail, item.get('EmailTo')
            text_content = 'Dear %s \n\n  This is first reminder regarding payment of the attached invoice. \nWe kindly ask you to complete payment of the invoice directly, and to inform us about the payment by replying to this email. \n\n Kind regards, \n The %s Team' % (item.get('SendToName'), location_name)
            html_content = '''
            <html><head><style> body { font: 12px 'Open Sans', Tahoma, Arial; color: #000000; } </style></head>
            <body>
            <p>
            Dear %s </br></br>
            This is first reminder regarding payment of the attached invoice. </br>
            We kindly ask you to complete payment of the invoice directly, and to inform us about the payment by replying to this email. </br></br>
            Kind regards, </br>
            The %s Team
            </p>
            <body></html>
            '''  % (item.get('SendToName'), location_name)
    
        elif status == 2:
            subject, from_email, to = '%s invoice %s - second reminder' % (location_name, item.get('Code')), location_admin_mail, item.get('EmailTo') 
            text_content = 'Dear %s \n\n  This is second reminder regarding payment of the attached invoice. \nWe kindly ask you to complete payment of the invoice directly, and to inform us about the payment by replying to this email. \n\n Kind regards, \n The %s Team' % (item.get('SendToName'), location_name)
            html_content = '''
            <html><head><style> body { font: 12px 'Open Sans', Tahoma, Arial; color: #000000; } </style></head>
            <body>
            <p>
            Dear %s </br></br>
            This is second reminder regarding payment of the attached invoice. </br>
            We kindly ask you to complete payment of the invoice directly, and to inform us about the payment by replying to this email. </br></br>
            Kind regards, </br>
            The %s Team
            </p>
            <body></html>
            '''  % (item.get('SendToName'), location_name)
            
        elif status == 3:
            subject, from_email, to = '%s invoice %s - THIRD REMINDER' % (location_name, item.get('Code')), location_admin_mail, item.get('EmailTo')
            text_content = 'Dear %s \n\n  This is third reminder regarding payment of the attached invoice. \nWe kindly ask you to complete payment of the invoice directly, and to inform us about the payment by replying to this email. \n\n Kind regards, \n The %s Team' % (item.get('SendToName'), location_name)
            html_content = '''
            <html><head><style> body { font: 12px 'Open Sans', Tahoma, Arial; color: #000000; } </style></head>
            <body>
            <p>
            Dear %s </br></br>
            This is third reminder regarding payment of the attached invoice. </br>
            We kindly ask you to complete payment of the invoice directly, and to inform us about the payment by replying to this email. </br></br>
            Kind regards, </br>
            The %s Team
            </p>
            <body></html>
            '''  % (item.get('SendToName'), location_name)
            
        elif status == 4:
            subject, from_email, to = '%s invoice %s - FOURTH AND FINAL NOTICE' % (location_name, item.get('Code')), location_admin_mail, item.get('EmailTo')
            text_content = 'Dear %s \n\n  This is fourth and final notice regarding payment of the attached invoice. \nWe kindly ask you to complete payment of the invoice directly, and to inform us about the payment by replying to this email. \n\n Kind regards, \n The %s Team' % (item.get('SendToName'), location_name)
            html_content = '''
            <html><head><style> body { font: 12px 'Open Sans', Tahoma, Arial; color: #000000; } </style></head>
            <body>
            <p>
            Dear %s </br></br>
            This is fourth and final reminder regarding payment of the attached invoice. </br>
            We kindly ask you to complete payment of the invoice directly, and to inform us about the payment by replying to this email. </br></br>
            Kind regards, </br>
            The %s Team
            </p>
            <body></html>
            '''  % (item.get('SendToName'), location_name)
                
        file_to_be_sent = self.show_invoice(item.get('Id')).getvalue()
        email = EmailMultiAlternatives(subject, text_content, from_email, [to])
        email.attach("Invoice.pdf", file_to_be_sent, "application/pdf")
        email.attach_alternative(html_content, "text/html")
        try:
            email.send()
        except: #The email can't be sent, send admin a message
            subject, from_email, to = 'Invoice reminder cannot be sent %s' % item.get('Code'), 'felix@donfelicio.com', location_admin_mail
            text_content = 'Dear admin \n\n  The invoice reminder could not be sent. Maybe the email address is missing, or another error occured.'
            html_content = '''
            <html><head><style> body { font: 12px 'Open Sans', Tahoma, Arial; color: #000000; } </style></head>
            <body>
            <p>
            Dear Admin </br></br>
            The invoice reminder could not be sent. Maybe the email address is missing, or another error occured.
            </p>
            <body></html>
            '''
            file_to_be_sent = self.show_invoice(item.get('Id')).getvalue()
            email = EmailMultiAlternatives(subject, text_content, from_email, [to])
            email.attach("Invoice.pdf", file_to_be_sent, "application/pdf")
            email.attach_alternative(html_content, "text/html")
            email.send()
        else: #the email was sent
            pass
    
        
        
        
        #and send to location admin
        if status == 3 or status == 4:
            
            subject, from_email, to = '%s invoice %s - reminder number: %sth out of 4' % (location_name, item.get('Code'), status), 'felix@donfelicio.com', location_admin_mail #from donfelicio.com 
            text_content = 'Dear admin \n\n  The invoice attached to this email has been reminded %s times now. Please give them a call to find out if anything is missing.' % status
            html_content = '''
            <html><head><style> body { font: 12px 'Open Sans', Tahoma, Arial; color: #000000; } </style></head>
            <body>
            <p>
            Dear admin </br></br>  The invoice attached to this email has been reminded %s times now. </br>
            Please give them a call to find out if anything is missing.
            </p>
            <body></html>
            ''' % status
            admin_email = EmailMultiAlternatives(subject, text_content, from_email, [to])
            admin_email.attach("Invoice.pdf", file_to_be_sent, "application/pdf")
            admin_email.attach_alternative(html_content, "text/html")
            admin_email.send()
    
    
    
    def handle(self, *args, **options):
        
        for item in self.s2m_get_invoicelist():
            # do NOT send to tax exempt people where the system thinks their tax still needs to be paid
            taxes = item.get('TotalIncludingTax') - item.get('TotalExcludingTax')
            if item.get('NoTax') == True and round(taxes,0) == round(item.get('AmountOpen'),0):
                pass #
            elif item.get('AmountOpen') < 1.00: #als minder dan 1 euro openstaat.
                print item.get('EmailTo')
                print item.get('Code')
                pass 
            else:#send them a fucking email
                two_weeks_after = datetime.datetime.strptime(str(item.get("ExpirationDate").split("T")[0]), '%Y-%m-%d') + datetime.timedelta(weeks=2)
                four_weeks_after = datetime.datetime.strptime(str(item.get("ExpirationDate").split("T")[0]), '%Y-%m-%d') + datetime.timedelta(weeks=4)
                six_weeks_after = datetime.datetime.strptime(str(item.get("ExpirationDate").split("T")[0]), '%Y-%m-%d') + datetime.timedelta(weeks=6)
                eight_weeks_after = datetime.datetime.strptime(str(item.get("ExpirationDate").split("T")[0]), '%Y-%m-%d') + datetime.timedelta(weeks=8)
                
                instance, created = Invoicereminder.objects.get_or_create(invoice_id=item.get('Id'))        
                invoice_reminder = Invoicereminder.objects.get(invoice_id=item.get('Id')).invoice_status    
                
                #send 1st reminder
                if datetime.datetime.today() > two_weeks_after and datetime.datetime.today() < four_weeks_after and invoice_reminder != 1:
                    print 'stuur deze 1e %s' % item.get('ExpirationDate')
                    self.email_to_send(1, item)  #EMAIL sending is done here
                #then update database two_weeks instance to yes.
                    instance.invoice_status = 1
                    instance.save()
                
                #send 2nd reminder
                if datetime.datetime.today() >= four_weeks_after and datetime.datetime.today() <= six_weeks_after and invoice_reminder != 2:
                    print 'stuur deze 2e %s' % item.get('ExpirationDate')
                    self.email_to_send(2, item)  #EMAIL sending is done here
                #then update database two_weeks instance to yes.
                    instance.invoice_status = 2
                    instance.save()
                
                #send 3rd reminder en naar infomail
                if datetime.datetime.today() >= six_weeks_after and datetime.datetime.today() <= eight_weeks_after and invoice_reminder != 3:
                    print 'stuur deze 3e %s' % item.get('ExpirationDate')
                    self.email_to_send(3, item)   #EMAIL sending is done here
                #then update database two_weeks instance to yes.
                    instance.invoice_status = 3
                    instance.save()
                
                #send last notice en naar infomail
                if datetime.datetime.today() >= eight_weeks_after and invoice_reminder != 4:
                    print 'stuur deze 4e %s' % (item.get('ExpirationDate'))
                    self.email_to_send(4, item)   #EMAIL sending is done here
                #then update database two_weeks instance to yes.
                    instance.invoice_status = 4
                    instance.save()       

