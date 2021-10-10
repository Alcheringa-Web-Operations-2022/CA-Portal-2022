from django.urls import path
from submissions import views
from django.contrib.auth import views as auth_views
from .views import IdeaCreateView,POCCreateView,MediaCreateView,POCBulkCreateView

urlpatterns = [
    path('home/', views.home, name='submissionhome'),
    path('tasks/', views.tasks, name='tasks'),
    path('ideas/', views.ideas, name='ideas'),
    path('poc/', views.pocs, name='pocs'),      
    path('idea/new/', IdeaCreateView.as_view(), name='idea-create'),
    path('poc/new/', POCCreateView.as_view(), name='poc-create'),
    path('poc/newcsv/',POCBulkCreateView.as_view(), name='poc-csv-create'),
    path('media/new/', MediaCreateView.as_view(), name='media-create'),
]
