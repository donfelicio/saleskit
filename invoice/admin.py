from django.contrib import admin
from .models import *

class Invoicereminderadmin(admin.ModelAdmin):
    list_display = ['invoice_id', 'invoice_status', 'date_updated']
    class Meta:
        model = Invoicereminder
        
admin.site.register(Invoicereminder, Invoicereminderadmin)