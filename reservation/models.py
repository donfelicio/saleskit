from django.db import models
import datetime

# Create your models here.

class Reservation(models.Model):
    res_id = models.CharField(max_length = 255)
    res_user = models.CharField(max_length = 255, null=True)
    res_location_id = models.CharField(max_length = 255, null=True)    
    res_company = models.CharField(max_length = 255)
    res_desc = models.CharField(max_length = 255)
    res_date_created = models.DateField()
    res_date = models.DateField()
    res_status_choices = {
        ('1', 'attention required'),
        ('2', 'final'),
        ('3', 'cancelled')
    }
    res_status = models.CharField(max_length = 255, choices=res_status_choices, default='1')
    res_status_sales_choices = (
        ('1', 'Request received'),
        ('2', 'Called customer'),
        ('3', 'Location tour planned'),
        ('4', 'Sent offer'),
        ('5', 'Called about offer'),
        ('6', 'Prepared meeting'),
        ('7', 'Aftersales'),
        ('8', 'Deal success'),
        ('9', 'Deal failed'),   
    )
    res_status_sales = models.CharField(max_length = 255, choices=res_status_sales_choices, default='1')
    res_total_seats = models.CharField(max_length = 255, null=True)
    res_prev_status = models.CharField(max_length = 255,choices=res_status_sales_choices, default='9')
    res_last_change_by = models.CharField(max_length = 255, null=True)
    res_last_change_date = models.DateField(auto_now = True)
    res_intro = models.TextField(null=True, default='')
    class Meta:
        ordering = ['res_date', 'res_id']   

class Statuscode(models.Model):
    status_code = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    description_short = models.CharField(max_length = 255)
    class Meta:
        ordering = ['status_code']

class Userlocation(models.Model):
    location_id = models.CharField(max_length = 255, null=True)
    user_name = models.CharField(max_length = 255, null=True)
    location_name = models.CharField(max_length = 255, null=True)
    
class Userprofile(models.Model):
    user_name = models.CharField(max_length = 255, null=True)
    user_key = models.CharField(max_length = 255, null=True)
    active_location = models.CharField(max_length = 255, default=False)
    last_login = models.DateField(auto_now=True, null=True)
    res_updated = models.CharField(max_length = 255, default='no')
    loc_updated = models.CharField(max_length = 255, default='no')
    
class Reservationfilter(models.Model):
    res_id = models.CharField(max_length = 255, null=True)
    user_name = models.CharField(max_length = 255, null=True)
    hide_days = models.DateField(null=True)
    
class Loginlog(models.Model):
    user_name = models.CharField(max_length = 255, null=True)
    login_date = models.DateTimeField(auto_now=True, null=True)
    
class Statuschange(models.Model):
    user_name = models.CharField(max_length = 255, null=True)
    change_date = models.DateTimeField(auto_now=True, null=True)
    res_id = models.CharField(max_length = 255, null=True)
    res_status_sales_code = models.CharField(max_length = 255, null=True)
    res_status_sales = models.CharField(max_length = 255, null=True)
    change_note = models.TextField(null=True, default='')
    class Meta:
        ordering = ['-res_status_sales_code']
    
    