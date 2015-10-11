from django.db import models

# Create your models here.

class Reservation(models.Model):
    res_id = models.CharField(max_length = 255, unique=True)
    res_user = models.CharField(max_length = 255, null=True)
    res_location_id = models.CharField(max_length = 255, null=True)    
    res_company = models.CharField(max_length = 255)
    res_desc = models.CharField(max_length = 255)
    res_date_created = models.DateField()
    res_date = models.CharField(max_length = 255)
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
    res_last_action_taken = models.DateField()
    res_untouched = models.CharField(max_length = 255, default='yes')
    class Meta:
        ordering = ['res_date']
        

class Statuscode(models.Model):
    status_code = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    description_short = models.CharField(max_length = 255)


    
class Filteroption(models.Model):
    filter_name = models.CharField(max_length = 255, null=True)
    filter_short = models.CharField(max_length = 255, null=True)
    filter_desc = models.CharField(max_length = 255, null=True)
    filter_status = models.IntegerField()


    