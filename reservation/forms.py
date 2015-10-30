from django import forms
from reservation.models import *
import datetime

class ReservationfilterForm(forms.ModelForm):
    class Meta:
        model = Reservationfilter
        fields = ['res_id', 'user_name', 'hide_days']
        
class UpdateprofileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['user_name', 'active_location']
        