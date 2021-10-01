from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import PostCreateView,POCCreateView

urlpatterns = [
    path('home/', views.home, name='home'),
    path('ideas/', views.ideas, name='ideas'),
    path('poc/', views.poc,name="poc"),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('poc/new/', POCCreateView.as_view(), name='poc-create'),
    path('poc/new_csv/',views.uploadcsv, name='poc-csv-create'),
]
