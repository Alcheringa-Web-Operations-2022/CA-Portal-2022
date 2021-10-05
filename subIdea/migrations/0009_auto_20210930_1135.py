# Generated by Django 3.2.7 on 2021-09-30 06:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subIdea', '0008_tasks_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='ideaDueData',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='tasks',
            name='pocDueData',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='tasks',
            name='socialDueData',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]