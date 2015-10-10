from django import forms
from reservation.models import *

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['res_id', 'res_status_sales']
        
class TouchedForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['res_untouched']
        
class UpdateFilter(forms.ModelForm):
    class Meta:
        model = Filteroption
        fields = ['filter_name', 'filter_status']
        