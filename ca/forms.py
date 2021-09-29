from django import forms
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_module


class POCForm(UserCreationForm):
  
    poc_name = forms.CharField(label="POC NAME")
    poc_design = forms.CharField(label="POC DESIGNATION")
    poc_college = forms.CharField(label="POC COLLEGE")
    poc_phone = PhoneNumberField(label="POC CONTACT' required=False))
    
    class Meta:
        model = User
        fields = ['poc_name','poc_design','poc_college,'poc_phone']


