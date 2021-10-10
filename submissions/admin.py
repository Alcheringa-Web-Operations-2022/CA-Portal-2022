from django.contrib import admin
from .models import POC, POCBulk,Submission,Idea,Media
# Register your models here.

admin.site.register(POC)
admin.site.register(POCBulk)
admin.site.register(Idea)
admin.site.register(Media)
