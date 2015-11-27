from django.contrib import admin
from .models import *

class Invoicereminderadmin(admin.ModelAdmin):
    list_display = ['invoice_id', 'invoice_status', 'date_updated']
    class Meta:
        model = Invoicereminder
        
admin.site.register(Invoicereminder, Invoicereminderadmin)

class Activelocationadmin(admin.ModelAdmin):
    list_display = ['location_id', 'profile_key']
    class Meta:
        model = Activelocation
        
admin.site.register(Activelocation, Activelocationadmin)