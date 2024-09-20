from django import forms
from .models import *
from django.contrib.auth.models import Group  
from users.models import District


class MemberForm(forms.ModelForm):
    departmentID=forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Choose Department To Join", to_field_name="id")
    class Meta:
        model=Member
        fields='__all__'
        exclude=['department']
        
        
        
class DistrictForm(forms.ModelForm):
    class Meta:
        model=District
        fields='__all__'
