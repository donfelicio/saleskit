from django.contrib import admin

# Register your models here.
from .models import *


class Reservationadmin(admin.ModelAdmin):
    list_display = ['res_id', 'res_user', 'res_date', 'res_location_id', 'res_date_created', 'res_status_sales']
    search_fields = ['res_id']
    class Meta:
        model = Reservation
        
admin.site.register(Reservation, Reservationadmin)

class Statuscodeadmin(admin.ModelAdmin):
    list_display = ['status_code', 'description', 'description_short']
    class Meta:
        model = Statuscode
        
admin.site.register(Statuscode, Statuscodeadmin)

class Userlocationadmin(admin.ModelAdmin):
    list_display = ['location_id', 'location_name', 'user_name']
    class Meta:
        model = Userlocation
        
admin.site.register(Userlocation, Userlocationadmin)

class Userprofileadmin(admin.ModelAdmin):
    list_display = ['user_name', 'active_location', 'last_login']
    class Meta:
        model = Userprofile
        
admin.site.register(Userprofile, Userprofileadmin)

class Reservationfilteradmin(admin.ModelAdmin):
    list_display = ['res_id', 'user_name', 'hide_days']
    class Meta:
        model = Reservationfilter
        
admin.site.register(Reservationfilter, Reservationfilteradmin)

class Loginlogadmin(admin.ModelAdmin):
    list_display = ['user_name', 'login_date']
    class Meta:
        model = Loginlog
        
admin.site.register(Loginlog, Loginlogadmin)
