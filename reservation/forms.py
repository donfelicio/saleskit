from django import forms
from reservation.models import *
import datetime

class UpdateprofileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['user_name', 'active_location']
        