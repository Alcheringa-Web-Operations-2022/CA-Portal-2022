from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views
from .views import VerificationView

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/', user_views.loginPage, name='login'),
    path('profile/', user_views.profile, name='profile'),
    path('googleauth/', user_views.googleauth, name='googleauth'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate"),
    # Password reset urls
    path("password_reset", user_views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password/password_reset_complete.html'), name='password_reset_complete'),
]
