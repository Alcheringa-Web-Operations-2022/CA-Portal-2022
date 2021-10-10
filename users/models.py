import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from .utils import create_new_ref_number
from PIL import Image


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, firstname, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('username', 'superuser')
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user(email,  firstname, password, "email", **other_fields)

    def create_user(self, email, firstname, password, provider, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          firstname=firstname, provider=provider, ** other_fields)
        user.set_password(password)
        user.save()
        return user


# Username for admin is admin, superuser is superuser
# firstname field stores the user full name of the User


class NewUser(AbstractBaseUser, PermissionsMixin):
    id = models.SlugField(primary_key=True, default=uuid.uuid4)
    alcherid = models.CharField(
        max_length=9, blank=True, unique=True, default=create_new_ref_number)
    
    img = models.ImageField(
        upload_to="image-uploads/", default='image-uploads/user.png')
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=False, default="user")
    firstname = models.CharField(max_length=150, blank=True)
    phone = PhoneNumberField(unique=False, blank=True)
    graduation_year = models.CharField(max_length=200, unique=False)
    college_state = models.CharField(max_length=200, unique=False)
    college_city = models.CharField(max_length=200, unique=False)
    college_name = models.CharField(max_length=200, unique=False)
    position_of_responsibility = models.CharField(
        max_length=200, unique=False, blank=True)
    interested_modules = models.CharField(
        max_length=200, unique=False, blank=True)
    # Referral fields
    referred_by = models.CharField(
        max_length=9, blank=True)
    # referred_by_user = models.ForeignKey(
    #     'NewUser', blank=True, on_delete=models.CASCADE)
    referrals = models.IntegerField(default=0)
    # other fields

    date_joined = models.DateTimeField(default=timezone.now)
    provider = models.CharField(max_length=200, unique=False, default="email")
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = CustomAccountManager()
    points = models.IntegerField(default=0)
    tasks = models.IntegerField(default=0)
    instahandle = models.CharField(max_length=200, unique=True, default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname']

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.img.path)
        width, height = img.size  # Get dimensions

        if width > 300 and height > 300:
            # keep ratio but shrink down
            img.thumbnail((width, height))

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.img.path)
        


class UserSingle(models.Model):
    user = models.ForeignKey('NewUser', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.id} Profile'


class UserGroup(models.Model):
    id = models.SlugField(primary_key=True, default=uuid.uuid4)
    leader = models.ForeignKey(
        'NewUser', related_name='leader', on_delete=models.CASCADE)
    executive = models.ForeignKey(
        'NewUser', related_name='executive', on_delete=models.CASCADE)
    college_state = models.CharField(max_length=200, unique=False)
    college_city = models.CharField(max_length=200, unique=False)
    college_name = models.CharField(max_length=200, unique=False)

    referred_by = models.CharField(
        max_length=9, blank=True)
    # referred_by_user = models.ForeignKey(
    #     'NewUser', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
