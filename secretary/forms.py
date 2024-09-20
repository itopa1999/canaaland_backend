from django import forms
from .models import *
from django.contrib.auth.models import Group  
from .models import *


class ChurchMemberForm(forms.ModelForm):
    class Meta:
        model=Church_Member
        exclude=['district']
        
        
        
class ChurchNewMemberForm(forms.ModelForm):
    class Meta:
        model=Church_New_Member
        exclude=['district']
        
        
class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        exclude=['district','date']
        
        
class DistrictAttendanceForm(forms.ModelForm):
    class Meta:
        model=Church_Attendance
        exclude=['district','date']
        
        