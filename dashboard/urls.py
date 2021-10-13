from django.urls import path
from dashboard import views as dashboard_views
urlpatterns = [
    path('', dashboard_views.dashboard, name='dashboard_page'),
    path('contactus', dashboard_views.contactus, name='contactus'),
    path('checkLike', dashboard_views.verify_like, name='verifymylike'),
]
