from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ShareablePost
from django.contrib import messages
from submissions.models import Media
from datetime import datetime
from django.db.models import Exists,OuterRef
from submissions.models import Idea
from .models import Notifications
from django.db.models import Q
def dashboard(request):
    if request.user.is_authenticated:
        post_list = ShareablePost.objects.all().order_by('-created_on'
        ).exclude(last_date__lt=datetime.now().date()
        ).annotate(is_shared=Exists(Media.objects.filter(
            shared_post__id=OuterRef('id'),
            user=request.user,
            ))
        ).exclude(is_shared=True)
        # Notifications List
        notification_list = Notifications.objects.filter(Q(user=request.user) | Q(user=None)).order_by('-created_on')
        context = {
            'post_list': post_list,
            'heading':'Dashboard',
            'notification_list': notification_list
        }
        return render(request, 'dashboard/dashboard_page.html',context)
    else:
        return render(request, 'dashboard/landing_page.html')

def verify_like(request):

    
    from instagram_private_api import Client
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
        user_name = 'fun_tas_tic_12'
        password = 'Qwerty@123'
        api = Client(user_name, password)
        results = api.media_likers_chrono('2636572187229882088_1537399767')
        items = results['users']
        flag=0
        for item in items: 
            if item['username'] == request.user.instahandle:
                flag=1
                break
        
        if flag==1:
            request.user.points+=25
            request.user.save()
            messages.success(request,"Thank you for liking this post! You have gained 25 points")
            post.likedusers+=request.user.instahandle+' '
            post.save()
        else:
            messages.warning(request,"Looks like you haven't liked this post yet!")
    return redirect('dashboard_page')

