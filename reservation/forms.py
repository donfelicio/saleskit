from django import forms
from reservation.models import *
import datetime

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['res_id', 'res_status_sales', 'res_prev_status', 'res_last_change_by']
        
class HidereservationForm(forms.ModelForm):
    class Meta:
        model = Hidereservation
        fields = ['res_id', 'user_name', 'hide_days']
        
class UpdateprofileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['user_name', 'active_location']
        