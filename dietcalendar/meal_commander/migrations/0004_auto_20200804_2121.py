# Generated by Django 3.0.8 on 2020-08-04 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meal_commander', '0003_auto_20200804_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='DietIngredientQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='dish',
            name='ingredient_id',
            field=models.ManyToManyField(to='meal_commander.Ingredient'),
        ),
        migrations.DeleteModel(
            name='Diet',
        ),
        migrations.AddField(
            model_name='dietingredientquantity',
            name='dish_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='meal_commander.Dish'),
        ),
        migrations.AddField(
            model_name='dietingredientquantity',
            name='ingredient_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='meal_commander.Ingredient'),
        ),
    ]