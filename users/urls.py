from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views

from .views import VerificationView

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/', user_views.loginPage, name='login'),
    path('profile/', user_views.Profile, name='profile'),
    path('googleauth/', user_views.googleauth, name='googleauth'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate")
]
