from django.urls import path 
from . import views


app_name = 'ca'

urlpatterns = [
    path('poc-upload-csv/', views.poc, name='poc'),
    path('poc-upload/', views.poc_form, name='poc_form'),
    
   
]
