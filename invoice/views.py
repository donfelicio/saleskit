from django.shortcuts import render
import time, datetime, json, requests
from django.shortcuts import redirect, render
import cStringIO as StringIO #start pdf creation imports
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape #end pdf creation imports

##LET OP
#hij haalt ook alles op waarbij gebruiker BTW vrijgesteld is, die dus niet reminden..

 
#NB: rowsleft doesn't work here, API doesn't show rows but a count of all items. 
def s2m_get_invoices(request):
    page = 1 #!!!!change to 1 after testen
    items = 1 #must define but can't be zero:)
    results=[]
    total = 0
    rowsleft = 10000
#    while rowsleft > -20:
    url = 'http://www.seats2meet.com/api/invoices/location/563'
    headers = {'content-type':'application/json', 'Connection':'close'}
    data = {
    "ApiKey":91216637,
    "ProfileKey":"6DE79403-D5EF-186C-9529-25ED04A66FD6",
    "SearchTerm":"",
    "Page":page,
    "ItemsPerPage":items,
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
    results.extend(r)
    #up page 1
    page += 1
    for var in r:
        total = total + var.get("AmountOpen")
    
    if rowsleft == 10000:
        for var in r[:1]:
            rowsleft = var.get("MoreRows") - items       
    else:
        rowsleft -= items
    print rowsleft
    return results



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
    context = {
        'invoices': s2m_get_invoices(request)
        }
    template = 'invoice.html'
    return render(request, template, context)