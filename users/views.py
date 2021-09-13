from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.urls import reverse
from .models import NewUser
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.views import View


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
                messages.success(request, ('Registration successful. Check your mail for the link to verify your account.'))
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
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard_page')
            else:
                print("errrr")
                messages.error(request, 'Username OR password is incorrect') 
        return render(request, 'users/login.html')


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
