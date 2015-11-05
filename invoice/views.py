from django.shortcuts import render
import time, datetime, json, requests
from datetime import date
from django.shortcuts import redirect, render
import cStringIO as StringIO #start pdf creation imports
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape #end pdf creation imports


##LET OP
#hij haalt ook alles op waarbij gebruiker BTW vrijgesteld is, die dus niet reminden..
#check gewoon of BTW gelijk is aan AMountopen, dan passen..
def escape(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    return html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace("&#39;", '\'')
 
#NB: rowsleft doesn't work here, API doesn't show rows but a count of all items. 
def s2m_get_invoices(request):

#    while rowsleft > -20:
    url = 'http://www.seats2meet.com/api/invoices/112373'
    headers = {'content-type':'application/json', 'Connection':'close'}
    data = {
    "ApiKey":91216637,
    "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    "SearchTerm":"",
    "StatusIds":[],
    "StartDate":str(datetime.date.today() - datetime.timedelta(weeks=156)),
    "EndDate":str(datetime.date.today() + datetime.timedelta(weeks=52)),
    "UnPaidOnly":True,
    "IsDeposit":False,
    "LocationId":"563",    
    }
    
    r = requests.get(url, params=json.dumps(data), headers=headers)
    print r.text
    r = json.loads(r.text) 
    return r


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


        
        
def home(request):
    invoice = s2m_get_invoices(request)
    
    context = {
        'invoice': invoice,
        'footer': escape(invoice.get('Footer').replace('\"','')),
        'activation_date': datetime.datetime.strptime(str(invoice.get('ActivationDate').split("T")[0]), '%Y-%m-%d').strftime('%d-%b-%Y'),
        'expiration_date': datetime.datetime.strptime(str(invoice.get('ExpirationDate').split("T")[0]), '%Y-%m-%d').strftime('%d-%b-%Y'),
        'reservation_date': datetime.datetime.strptime(str(invoice.get('InvoiceReferences')[0].get('ReservationDate').split("T")[0]), '%Y-%m-%d').strftime('%d-%b-%Y'),
        }
    template = 'invoice.html'
    
    #return render_to_pdf(template, context)
     
    return render(request, template, context)