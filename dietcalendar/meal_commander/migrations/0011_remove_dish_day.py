# Generated by Django 3.0.8 on 2020-08-14 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal_commander', '0010_plan_actual_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='day',
        ),
    ]
