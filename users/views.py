from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import NewUser
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q


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
                subject = "Activate your account"
                email_template_name = "users/email_verify_mail.txt"
                firstname = request.POST.get('firstname')
                c = {
                    "firstname": firstname,
                    "link": 'https://'+domain+link,
                    }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'Alcheringa Campus Ambassador <schedulerevent9@gmail.com>', [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
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
                    messages.error(request, 'This email is registered with another provider')
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
                    messages.error(request, 'Email is registered with another provider or the email is not activated')
                    return HttpResponse('Email is registered with another provider or the email is not activated') 
            else:
                myuser = NewUser.objects.create_user(email, firstname, password, "google")
                myuser.save()
                messages.success(request, 'Registration successful. Check your mail for the link to update your account')
                user = NewUser.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user)})
                subject = "Activate your account"
                email_template_name = "users/email_verify_mail.txt"
                firstname = request.GET.get('firstname')
                c = {
                    "firstname": firstname,
                    "link": 'https://'+domain+link,
                    }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'Alcheringa Campus Ambassador <schedulerevent9@gmail.com>', [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found. Try again')
                return HttpResponse('Registration successful. Check your mail for the link to update your account')


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
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your Profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'title': 'profile', 'u_form':u_form})


def password_reset_request(request):
    User = get_user_model()
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data, provider="email"))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "users/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Alcheringa Web Operations',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'Alcheringa Campus Ambassador <schedulerevent9@gmail.com>', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, ("Password reset mail sent successfully."))
            else:
                messages.error(request, ("Email not registered with us"))
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="users/password/password_reset.html", context={"password_reset_form":password_reset_form})

