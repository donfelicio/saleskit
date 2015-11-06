from django.db import models

# Create your models here.

class Invoicereminder(models.Model):
    invoice_id = models.CharField(max_length=255, null=True)
    invoice_status = models.IntegerField(default=0)
    sent_stage = models.CharField(max_length=255, default='no')
    
    