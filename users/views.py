from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SingleUserRegisterForm, GroupUserRegisterForm, GroupUserRegisterFormForSingle, UserUpdateForm
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
from .models import UserSingle
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
User = get_user_model()

def register_single_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')
    else:
        single_user_form = SingleUserRegisterForm(request.POST or None)
        if request.method == 'POST':
            if single_user_form.is_valid():
                result = single_user_form.save(commit=False)

                if(request.POST.get('referred_by')):
                    user = NewUser.objects.get(
                        alcherid=request.POST.get('referred_by'))
                    # result.referred_by_user=user
                    result.points = 25
                    result.save()
                    user.referrals += 1
                    user.points += 25
                    user.save()
                else:
                    result.save()

                user = NewUser.objects.get(email=request.POST.get('email'))
                userSingle = UserSingle()
                userSingle.user = user
                userSingle.save()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user)})
                subject = "Activate your account"
                email_template_name = "users/email_verify_mail.html"
                firstname = request.POST.get('firstname')
                c = {
                    "firstname": firstname,
                    "link": 'https://'+domain+link,
                }
                email = render_to_string(email_template_name, c)
                try:
                    message = EmailMultiAlternatives(
                        subject=subject,
                        body="mail testing",
                        from_email='Alcheringa Campus Ambassador <schedulerevent9@gmail.com>',
                        to=[user.email]
                    )
                    message.attach_alternative(email, "text/html")
                    message.send(fail_silently=False)

                    # send_mail(subject, email, 'Alcheringa Campus Ambassador <schedulerevent9@gmail.com>', [
                    #           user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(
                    request, ('Registration successful. Check your mail for the link to activate your account.'))
                return redirect('register_single')
        else:
            single_user_form = SingleUserRegisterForm()
        return render(request, 'users/register_single.html', {'single_user_register_form': single_user_form, })


def register_group_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')
    else:
        group_user_form = GroupUserRegisterForm(request.POST or None)
        single_user_form_1 = GroupUserRegisterFormForSingle(
            request.POST or None, prefix='form_1')
        single_user_form_2 = GroupUserRegisterFormForSingle(
            request.POST or None, prefix='form_2')
        if request.method == 'POST':
            if single_user_form_1.is_valid() and single_user_form_2.is_valid() and group_user_form.is_valid():
                single_form_1_result = single_user_form_1.save(commit=False)
                single_form_1_result.college_state = request.POST.get(
                    'college_state')
                single_form_1_result.college_city = request.POST.get(
                    'college_city')
                single_form_1_result.college_name = request.POST.get(
                    'college_name')
                single_form_1_result.referred_by = request.POST.get(
                    'referred_by')
                single_form_1_result.set_password(
                    request.POST.get('password1'))
                single_form_1_result.username = "Groupuser"
                single_form_1_result.save()
                # 2nd form
                single_form_2_result = single_user_form_2.save(commit=False)
                single_form_2_result.college_state = request.POST.get(
                    'college_state')
                single_form_2_result.college_city = request.POST.get(
                    'college_city')
                single_form_2_result.college_name = request.POST.get(
                    'college_name')
                single_form_2_result.referred_by = request.POST.get(
                    'referred_by')
                single_form_2_result.set_password(
                    request.POST.get('password1'))
                single_form_2_result.username = "Groupuser"
                single_form_2_result.save()

                user_1 = NewUser.objects.get(
                    email=request.POST.get('form_1-email'))
                user_2 = NewUser.objects.get(
                    email=request.POST.get('form_2-email'))

                group_form_result = group_user_form.save(commit=False)
                group_form_result.leader = user_1
                group_form_result.executive = user_2

                if(request.POST.get('referred_by')):
                    user = NewUser.objects.get(
                        alcherid=request.POST.get('referred_by'))
                    # result.referred_by_user=user
                    group_form_result.referred_by = request.POST.get(
                        'referred_by')
                    user.referrals += 1
                    user.save()
                    group_form_result.save()
                else:
                    group_form_result.save()
                # SEnding mail to leader

                uidb64 = urlsafe_base64_encode(force_bytes(user_1.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user_1)})
                subject = "Activate your account"
                email_template_name = "users/email_verify_mail.html"
                firstname = user_1.firstname
                c = {
                    "firstname": firstname,
                    "link": 'https://'+domain+link,
                }
                email1 = render_to_string(email_template_name, c)

                # sending mail to executive

                uidb64 = urlsafe_base64_encode(force_bytes(user_2.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user_2)})
                subject = "Activate your account"
                email_template_name = "users/email_verify_mail.html"
                firstname = user_2.firstname
                c = {
                    "firstname": firstname,
                    "link": 'https://'+domain+link,
                }
                email2 = render_to_string(email_template_name, c)
                try:
                    message = EmailMultiAlternatives(
                        subject=subject,
                        body="mail testing",
                        from_email='Alcheringa Campus Ambassador <schedulerevent9@gmail.com>',
                        to=[user_1.email]
                    )
                    message2 = EmailMultiAlternatives(
                        subject=subject,
                        body="mail testing",
                        from_email='Alcheringa Campus Ambassador <schedulerevent9@gmail.com>',
                        to=[user_2.email]
                    )
                    message.attach_alternative(email1, "text/html")
                    message.send(fail_silently=False)
                    message2.attach_alternative(email2, "text/html")
                    message2.send(fail_silently=False)
                    # send_mail(subject, email1, 'Alcheringa Campus Ambassador <schedulerevent9@gmail.com>', [
                    #           user_1.email], fail_silently=False)
                    # send_mail(subject, email2, 'Alcheringa Campus Ambassador <schedulerevent9@gmail.com>', [
                    #           user_2.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(
                    request, ('Registration successful. Check your mail for the link to activate your account.'))
                return redirect('register_group')
        # else:
        #     group_user_form = GroupUserRegisterForm()
        #     single_user_form_1 = GroupUserRegisterFormForSingle()
        #     single_user_form_2 = GroupUserRegisterFormForSingle()
        return render(request, 'users/register_group.html', {'group_user_register_form': group_user_form, 'single_user_register_form_1': single_user_form_1, 'single_user_register_form_2': single_user_form_2})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(email)
            user = NewUser.objects.filter(email=email)
            if(user):
                user = NewUser.objects.filter(email=email, provider="email")
                if user:
                    user = authenticate(
                        request, email=email, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('dashboard_page')
                    else:
                        print("errrr")
                        messages.error(
                            request, 'Password is incorrect for the email address entered or the email is not activated')
                else:
                    messages.error(
                        request, 'This email is registered with another provider')
            else:
                messages.error(request, 'Email is not registered')
        return HttpResponse("ok")




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
        u_form = UserUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your Profile has been updated!')
            return redirect('profile')
        print(u_form.errors)
    else:
        u_form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'heading': 'Profile', 'u_form': u_form})


def password_reset_request(request):
    User = get_user_model()
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(
                Q(email=data, provider="email"))
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
                        send_mail(subject, email, 'Alcheringa Campus Ambassador <schedulerevent9@gmail.com>', [
                                  user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(
                        request, ("Password reset mail sent successfully."))
            else:
                messages.error(request, ("Email not registered with us"))
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="users/password/password_reset.html", context={"password_reset_form": password_reset_form})
