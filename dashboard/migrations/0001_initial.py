# Generated by Django 3.1.2 on 2021-10-09 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareablePost',
            fields=[
                ('id', models.SlugField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('link_instagram', models.CharField(blank=True, max_length=500, null=True)),
                ('link_facebook', models.CharField(blank=True, max_length=500, null=True)),
                ('is_instagram', models.BooleanField(default=False)),
                ('is_facebook', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='image-uploads/')),
                ('caption', models.CharField(max_length=160)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.SlugField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('Success', 'Success'), ('Warning', 'Warning'), ('Info', 'Info')], max_length=200)),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
