from django.urls import path 
from . import views


app_name = 'ca'

urlpatterns = [
    path('poc-upload/', views.poc, name='poc'),
   
]