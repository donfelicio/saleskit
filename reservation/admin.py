from django.contrib import admin

# Register your models here.
from .models import *


class Reservationadmin(admin.ModelAdmin):
    list_display = ['res_id', 'res_user', 'res_date', 'res_date_created', 'res_status_sales', 'res_last_action_taken']
    class Meta:
        model = Reservation
        
admin.site.register(Reservation, Reservationadmin)

class Statuscodeadmin(admin.ModelAdmin):
    list_display = ['status_code', 'description', 'description_short']
    class Meta:
        model = Statuscode
        
admin.site.register(Statuscode, Statuscodeadmin)

class Filteroptionadmin(admin.ModelAdmin):
    list_display = ['filter_name', 'filter_desc', 'filter_status']
    class Meta:
        model = Filteroption
        
admin.site.register(Filteroption, Filteroptionadmin)
