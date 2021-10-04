from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    tell_us_your_idea = models.TextField()
    validate = models.BooleanField(default=0)
    submitdate = models.DateField(default=timezone.now)
    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('submissionhome')


class Tasks(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    ideaDone = models.BooleanField(default=0)
    pocDone = models.BooleanField(default=0)
    socialDone = models.BooleanField(default=0)
    points = models.IntegerField(default=0)
    ideaDueData = models.DateField(default=timezone.now)
    pocDueData = models.DateField(default=timezone.now)
    socialDueData = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.user)


def create_Tasks(sender,instance,created,**kwargs):
    if created:
        Tasks.objects.create(user=instance)
        print("Tasks created")

post_save.connect(create_Tasks, sender=User)