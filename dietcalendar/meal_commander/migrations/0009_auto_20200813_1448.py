# Generated by Django 3.0.8 on 2020-08-13 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal_commander', '0008_auto_20200807_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='actual_type',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='calendar_week',
        ),
    ]
