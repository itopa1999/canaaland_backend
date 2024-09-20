from django import forms
from .models import *
from django.contrib.auth.models import Group  
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm



class DistrictForm(forms.ModelForm):
    class Meta:
        model=District
        fields='__all__'
        
        
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email' ,'phone']
        exclude = ['password1','password2']


class UserCreationForm1(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email' ,'phone','district']
        exclude = ['password1','password2']   
        
class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email' ,'phone']
        exclude = ['password1','password2']