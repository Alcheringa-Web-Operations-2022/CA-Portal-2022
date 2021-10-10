from django.contrib import admin
from .models import Notifications, ShareablePost
# Register your models here.
admin.site.register(ShareablePost)
admin.site.register(Notifications)
