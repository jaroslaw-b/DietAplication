from django.db import models
from django.forms  import ModelForm, modelformset_factory
from django import forms
from django.urls import reverse

# Create your models here.
class Unit(models.Model):
	unit_type = models.CharField(max_length=10, unique=True)

	def __str__(self):
		return self.unit_type

class Ingredient(models.Model):
	name = models.CharField(max_length=25, unique=True)
	unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE)
	def __str__(self):
		return self.name

class Dish(models.Model):

	MEAL_TYPE_CHOICES = (
		(0, '1st breakfest'),
		(1, '2nd breakfest'),
		(2, 'Dinner'),
		(3, 'Supper'),
		)

	at_plan = models.IntegerField(default=0)
	name = models.CharField(max_length=30)
	meal_type = models.IntegerField(default=0, choices=MEAL_TYPE_CHOICES)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('dish')


class DietIngredientQuantity(models.Model):
	dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)
	ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0)
	def __str__(self):
		return self.dish_id.name + ": " + self.ingredient_id.name + " " + str(self.quantity) + self.ingredient_id.unit_id.unit_type
	class Meta:
		unique_together = ('dish_id', 'ingredient_id')

class Plan(models.Model):
	DAY_CHOICES = (
		(0 ,'Monday'),
		(1, 'Tuesday'),
		(2, 'Wednesday'),
		(3, 'Thursday'),
		(4, 'Friday'),
		(5, 'Saturday'),
		(6, 'Sunday'),
	)

	MEAL_TYPE_CHOICES = (
		(0, '1st breakfest'),
		(1, '2nd breakfest'),
		(2, 'Dinner'),
		(3, 'Supper'),
	)

	actual_day = models.IntegerField(default=0, choices=DAY_CHOICES)
	actual_type = models.IntegerField(default=0, choices=MEAL_TYPE_CHOICES)
	dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)

class PlanForm(ModelForm):
	class Meta:
		model = Plan
		fields = ['dish_id', 'actual_day', 'actual_type']
		widgets = {
			'dish_id' : forms.Select(
				attrs={'class' : 'form-control'}
				),
			'actual_day' : forms.Select(
				attrs={'class' : 'form-control'},
				),
			'actual_type' : forms.Select(
				attrs={'class' : 'form-control'},
				)
		}

class CalendarPlan(models.Model):
	MEAL_TYPE_CHOICES = (
		(0, '1st breakfest'),
		(1, '2nd breakfest'),
		(2, 'Dinner'),
		(3, 'Supper'),
	)

	meal_date = models.DateField()
	dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)
	actual_type = models.IntegerField(default=0, choices=MEAL_TYPE_CHOICES)

class CalendarPlanForm(ModelForm):
	class Meta:
		model=CalendarPlan
		fields = ['dish_id', 'meal_date', 'actual_type']
		widgets = {
			'dish_id' : forms.Select(
				attrs={'class' : 'form-control'}
				),
			'meal_date' : forms.DateInput(
				attrs={'class' : 'form-control'},
				),
			'actual_type' : forms.Select(
				attrs={'class' : 'form-control'},
				)
		}


class IngredientForm(ModelForm):
	class Meta:
		model = Ingredient
		fields = ['name', 'unit_id']
		widgets = {
			'name' : forms.TextInput(
				attrs={
				'class' : 'form-control',
				}
				),
			'unit_id' : forms.Select(
				attrs={
				'class' : 'form-control'
					},
				)
		}

DietIngredientQuantityFormSet = modelformset_factory(DietIngredientQuantity, exclude=('dish_id',) , fields=('ingredient_id', 'quantity'), extra=4, widgets = {
			'ingredient_id' : forms.Select(
				attrs={
				'class' : 'form-control selectpicker' ,
				'data-live-search' : "true",
				}
				),
			'quantity' : forms.NumberInput(
				attrs={
				'class' : 'form-control'
					},
				)},
			labels={
				'ingredient_id' : 'Ingredient',
				'quantity'		: 'Quantity'
			},
			)


class DishForm(ModelForm):
	class Meta:
		model = Dish
		fields = ['name', 'meal_type']
		widgets = {
			'name' : forms.TextInput(
				attrs={
				'class' : 'form-control',
				}
				),
			'meal_type' : forms.Select(
				attrs={
				'class' : 'form-control'
					},
				)
		}

