from logging import currentframe
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Promotions, ShareablePost
from users.models import UserGroup
from submissions.models import Media
from datetime import datetime
from django.db.models import Exists,OuterRef
from submissions.models import Idea
from .models import Notifications
from django.db.models import Q
from django.contrib import messages
from instagram_private_api import Client
import _datetime


""" start_time = _datetime.datetime.now().date()
user_name = 'a64guha'
password = 'Ankit@123#'
api = Client(user_name, password) """

def dashboard(request):
    if request.user.is_authenticated:
        post_list = ShareablePost.objects.all().order_by('-created_on'
        ).exclude(last_date__lt=datetime.now().date()
        ).annotate(is_shared=Exists(Media.objects.filter(
            shared_post__id=OuterRef('id'),
            user=request.user,
            ))
        ).exclude(is_shared=True)
        promotions = Promotions.objects.all().order_by('-created_on')
        # Notifications List
        isread=True
        notification_list = Notifications.objects.filter(Q(user=request.user) | Q(user=None)).order_by('-created_on')
        if list(UserGroup.objects.filter(leader=request.user)):
            grp_points = request.user.points + UserGroup.objects.filter(leader=request.user).first().executive.points
            grp_tasks = request.user.tasks + UserGroup.objects.filter(leader=request.user).first().executive.tasks
            grp_referrals = request.user.referrals + UserGroup.objects.filter(leader=request.user).first().executive.referrals
        elif list(UserGroup.objects.filter(executive=request.user)):
            grp_points = request.user.points + UserGroup.objects.filter(executive=request.user).first().executive.points
            grp_tasks = request.user.tasks + UserGroup.objects.filter(executive=request.user).first().executive.tasks
            grp_referrals = request.user.referrals + UserGroup.objects.filter(executive=request.user).first().executive.referrals
        else:
             grp_points = request.user.points
             grp_tasks = request.user.tasks
             grp_referrals = request.user.referrals
        for notif in notification_list:
            if not notif.isread:
                isread=False
                break

        context = {
            'post_list': post_list,
            'promotions': promotions,
            'heading':'Dashboard',
            'notification_list': notification_list,
            'grp_points':grp_points,
            'grp_tasks':grp_tasks,
            'grp_referrals':grp_referrals,

            'isread':isread
        }
        

        
        return render(request, 'dashboard/dashboard_page.html',context)
    else:
        return render(request, 'dashboard/landing_page.html')


@login_required
def contactus(request):
    if request.user.is_authenticated:
        # Notifications List
        notification_list = Notifications.objects.filter(
            Q(user=request.user) | Q(user=None)).order_by('-created_on')
        isread = True
        notification_list = Notifications.objects.filter(
            Q(user=request.user) | Q(user=None)).order_by('-created_on')
        for notif in notification_list:
            if not notif.isread:
                isread = False
                break
        context = {
            'heading': 'Contact us',
            'notification_list': notification_list, 'isread': isread
        }
        return render(request, 'dashboard/contactus.html', context)
    else:
        return render(request, 'dashboard/landing_page.html')

@login_required
def guidelines(request):
    if request.user.is_authenticated:
        # Notifications List
        notification_list = Notifications.objects.filter(
            Q(user=request.user) | Q(user=None)).order_by('-created_on')
        isread = True
        notification_list = Notifications.objects.filter(
            Q(user=request.user) | Q(user=None)).order_by('-created_on')
        for notif in notification_list:
            if not notif.isread:
                isread = False
                break
        context = {
            'heading': 'Guidelines',
            'notification_list': notification_list, 'isread': isread
        }
        return render(request, 'dashboard/guidelines.html', context)
    else:
        return render(request, 'dashboard/landing_page.html')

@login_required
def verify_like(request):

    
    """ print(start_time)
    post = ShareablePost.objects.get(id=str(list(request.GET.keys())[0]))
    check = 1
    if post.likedusers != '':
        arr = post.likedusers.split()
        for item in arr:
            if item==request.user.instahandle:
                check=0
                break
    if check == 0:
        messages.error(request,"You have already liked this post!")
    else:
        #api = auth.login_instagram('fun_tas_tic_12','Qwerty@123')
        
        curr_time=_datetime.datetime.now().date()
        delta = curr_time-start_time
        if delta.days >50:
            user_name = 'a64guha'
            password = 'Ankit@123#'
            api2 = Client(user_name, password)
            results = api2.media_likers_chrono(post.media_id)
        else:
            results = api.media_likers_chrono(post.media_id)
        items = results['users']
        flag=0
        
        for item in items: 
            print(item['username'])
            if item['username'] == request.user.instahandle:
                flag=1
                break
        
        if flag==1:
            request.user.points+=25
            request.user.tasks+=1
            request.user.save()
            messages.success(request,"Thank you for liking this post! You have gained 25 points")
            post.likedusers+=request.user.instahandle+' '
            post.save()
        else:
            messages.warning(request,"Looks like you have not liked this post yet!") """
    return redirect('dashboard_page') 

@login_required
def notif_unread(request):
    if request.method == 'PUT':
        notification_list = Notifications.objects.filter(
        Q(user=request.user) | Q(user=None)).order_by('-created_on')
        for notif in notification_list:
            if not notif.isread:
                notif.isread=True
                notif.save()
        return HttpResponse("OK")
