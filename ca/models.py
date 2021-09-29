 
from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError

def validate_sub(value):
	value=str(value)
	t=value.lower()
	if t.endswith(".pdf")!=True and t.endswith(".png")!=True and t.endswith(".jpg")!=True and t.endswith(".jpeg")!=True:
		raise ValidationError("Only above written Extensions are allowed.")
	else:	
		return value


class POC(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    design = models.CharField(max_length=60)
    college = models.CharField(max_length=90)
    contact = models.CharField(max_length=13)

def __str__(self):
		return f'{self.user.username}'

