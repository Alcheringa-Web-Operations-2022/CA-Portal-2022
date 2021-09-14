from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.urls import reverse
from .models import NewUser
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = NewUser.objects.get(email=request.POST.get('email'))
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = 'https://'+domain+link
                email_body = 'Hi '+request.POST.get('firstname') + \
                    ' Please use this link to verify your account\n' + activate_url
                email_subject = 'Activate your account'
                email = EmailMessage(
                    email_subject, email_body, 'Alcheringa Campus Ambassador <schedulerevent9@gmail.com>',
                    [request.POST.get('email')],
                )
                email.send(fail_silently=False)
                messages.success(request, ('Registration successful. Check your mail for the link to activate your account.'))
                return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = NewUser.objects.filter(email=email)
            if(user):
                user = NewUser.objects.filter(email=email, provider="email")
                if user:
                    user = authenticate(request, email=email, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('dashboard_page')
                    else:
                        print("errrr")
                        messages.error(request, 'Password is incorrect for the email address entered or the email is not activated') 
                else:
                    messages.error(request, 'This email is already authenticated with other provider')
            else:
                messages.error(request, 'Email is not registered')
        return render(request, 'users/login.html')

# authentication with google


def googleauth(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')
    else:
        if request.method == 'GET':
            email = request.GET.get('email')
            firstname = request.GET.get('firstname')
            password = "GOOGLEgoogle123"
            user = NewUser.objects.filter(email=email)
            if user:
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponse('Signed in successfully') 
                else:
                    return HttpResponse('Email is already signed in with another provider or the email is not activated') 
            else:
                myuser = NewUser.objects.create_user(email, firstname, password, "google")
                myuser.save()
                messages.success(request, 'Registration successful. Check your mail for the link to update your account')
                user = NewUser.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = 'https://'+domain+link
                email_body = 'Hi '+firstname + \
                    ' Please use this link to verify your account\n' + activate_url
                email_subject = 'Activate your account'
                email = EmailMessage(
                    email_subject, email_body, 'Alcheringa Campus Ambassador <schedulerevent9@gmail.com>',
                    [email],
                )
                email.send(fail_silently=False)
                return HttpResponse('Signed in duccessfully')


def logoutUser(request):
    logout(request)
    return redirect('login')


class VerificationView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = NewUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, NewUser.DoesNotExist):
            user = None
        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('dashboard_page')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            print("err")
            return redirect('dashboard_page')


@login_required
def Profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Ypur Account has been Updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }
    return render(request, 'users/profile.html', context)

