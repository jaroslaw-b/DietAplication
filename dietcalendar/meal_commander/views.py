from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.db.models import Count, Sum
from django.db.models import Prefetch
from django.db.models import prefetch_related_objects
import datetime
from .models import Dish, Ingredient, DietIngredientQuantity, Unit, IngredientForm, DietIngredientQuantityFormSet, DishForm, Plan, PlanForm, CalendarPlan, CalendarPlanForm

# Create your views here.
def index(request):

	num_dish = Dish.objects.all().count()
	num_ingredient = Ingredient.objects.all().count()
	context = {
        'num_dish': num_dish,
        'num_ingredients' : num_ingredient,
    }

	return render(request, 'index.html', context=context)

def dish(request):
	dish_list_1st_breakfest = Dish.objects.filter(meal_type=0)
	dish_list_2nd_breakfest = Dish.objects.filter(meal_type=1)
	dish_list_dinner = Dish.objects.filter(meal_type=2)
	dish_list_supper = Dish.objects.filter(meal_type=3)

	context = {
		'dish_list_1st_breakfest' : dish_list_1st_breakfest,
		'dish_list_2nd_breakfest' : dish_list_2nd_breakfest,
		'dish_list_dinner' : dish_list_dinner,
		'dish_list_supper' : dish_list_supper,

	}

	return render(request, 'dish.html', context=context)

def ingredient(request):
	ingredient_list = Ingredient.objects.order_by('name')

	context = {
		'ingredient_list' : ingredient_list,
	}

	return render(request, 'ingredient.html', context=context)

def ingredient_detail(request, ingredient_id):
	return HttpResponse("Widzisz szczegóły składnika o id %s" % ingredient_id)

def unit_detail(request, unit_id):
	return HttpResponse("Widzisz szczegóły jednostki o id %s" % unit_id)

def plan_detail(request, plan_id):
	return HttpResponse("Widzisz plan o id: %s", plan_id)

def dish_detail(request, dish_name):

	ingredient_list = DietIngredientQuantity.objects.filter(dish_id__name = dish_name)

	context = {
		'ingredient_list' : ingredient_list,
		'dish_name' : dish_name,
	}
	return render(request, 'dish_detail.html', context=context)

def add_dish_details(request, dish_name):
	if request.method == 'POST':	
		form = DietIngredientQuantityFormSet(request.POST)
		recipe = form.save(commit=False)

		for item in recipe:
			item.dish_id = Dish.objects.get(name=dish_name)
			item.save()

		return HttpResponseRedirect(reverse('dish'))
	else:
		form = DietIngredientQuantityFormSet(queryset=DietIngredientQuantity.objects.filter(dish_id=Dish.objects.get(name=dish_name)))
	
	context = {
		'formset' : form
	}
	return render(request, 'add_dish_details.html', context=context)

def add_ingredient(request):
	if request.method == 'POST':
		form = IngredientForm(request.POST, request.FILES)
		form.save()
		return HttpResponseRedirect(reverse('ingredient'))
	else:
		form = IngredientForm(initial = {'unit_id' : 1})

	context = {
		'form' : form,
	}

	return render(request, 'add_ingredient.html', context=context)


def add_dish(request, meal_type):
	if request.method == 'POST':
		form = DishForm(request.POST, request.FILES)
		form.save()
		return HttpResponseRedirect(reverse('dish'))
	else:
		form = DishForm(initial = {'meal_type' : meal_type})

	context = {
		'form' : form,
	}

	return render(request, 'add_dish.html', context=context)

def create_plan(request, day=-1, meal_type=-1, delete=0):

	dish_list_1st_breakfest = Plan.objects.filter(actual_type=0).order_by('actual_day')
	dish_list_2nd_breakfest = Plan.objects.filter(actual_type=1).order_by('actual_day')
	dish_list_dinner = Plan.objects.filter(actual_type=2).order_by('actual_day')
	dish_list_supper = Plan.objects.filter(actual_type=3).order_by('actual_day')
	
	#Delete meals from specified day and type
	if delete:
		Plan.objects.filter(actual_day=day, actual_type=meal_type).delete()
	
	if request.method == 'POST' and not delete:
		form = PlanForm(request.POST, request.FILES)
		form.save()
		return HttpResponseRedirect(reverse('create_plan'))
	#Handling GET request
	else:
		form = PlanForm(initial = {'actual_day' : day, 'actual_type' : meal_type})
		form.fields["dish_id"].queryset = Dish.objects.filter(meal_type=meal_type)
	

	q1 = []
	#Iteraring over all meals in plan to collect ingredients, quantity with units
	for e in Plan.objects.all():
		recipe = list(DietIngredientQuantity.objects.filter(dish_id=e.dish_id).values('ingredient_id__name', 'quantity', 'ingredient_id__unit_id__unit_type'))
		q1.append(recipe)
	
	#List flattening
	q1_list = [item for sublist in q1 for item in sublist]

	#Ordered lists of ingredients/quantities/units
	q1_list_ing = [ el['ingredient_id__name'] for el in q1_list]
	q1_list_quan = [ el['quantity'] for el in q1_list]
	q1_list_unit = [ el['ingredient_id__unit_id__unit_type'] for el in q1_list]

	#Ingredient quantity aggregation
	q1_list_ing_dict = {}
	for index,id_ in enumerate(q1_list_ing):
	    if id_ not in q1_list_ing_dict.keys():
	        q1_list_ing_dict[id_] = 0
	    q1_list_ing_dict[id_] = q1_list_ing_dict[id_] + q1_list_quan[index]

	#Matching units to ingredient
	shopping_list_to_template = []
	for key,val in q1_list_ing_dict.items():
		shopping_list_to_template.append("{0:40}".format(key) + str(val) + str(q1_list_unit[q1_list_ing.index(key)]))




	context = {
		'form' : form,
		'dish_list_1st_breakfest' : dish_list_1st_breakfest,
		'dish_list_2nd_breakfest' : dish_list_2nd_breakfest,
		'dish_list_dinner' : dish_list_dinner,
		'dish_list_supper' : dish_list_supper,
		'shopping_list' : shopping_list_to_template,
	}

	# When there is no specific meal to add generate plan view
	if day == -1 or delete == 1:
		return render(request, 'create_plan.html', context=context)
	# When day and/or meal type is specified, add new meal to plan
	else:
		return render(request, 'add_dish_to_weekplan.html', context=context)

def create_plan_calendar(request, calendar_year=-1, calendar_week=-1):

	year_now, week_now, day_now = datetime.datetime.now().isocalendar()
	if calendar_year == -1 and calendar_week == -1:
		calendar_year = year_now
		calendar_week = week_now

	dish_for_day = CalendarPlan.objects.filter(meal_date__year=calendar_year).filter(meal_date__week=calendar_week).order_by('meal_date')

	dish_list_1st_breakfest = dish_for_day.filter(actual_type=0)
	dish_list_2nd_breakfest = dish_for_day.filter(actual_type=1)
	dish_list_dinner = dish_for_day.filter(actual_type=2)
	dish_list_supper = dish_for_day.filter(actual_type=3)

	# List of all dates in current week
	current_week_start = datetime.datetime.fromisocalendar(calendar_year, calendar_week, 1)
	dates = [current_week_start + datetime.timedelta(days=i) for i in range(0 - current_week_start.weekday(), 7 - current_week_start.weekday())]
	
	# Handling 52/53 CW years
	last_week = datetime.date(calendar_year, 12, 28).isocalendar()[1]

	# Values for buttons (Prev week, current week, next week)
	next_week_year = {'week' : 1, 'year':calendar_year+1} if calendar_week == last_week else {'week' : calendar_week+1, 'year':calendar_year}
	previous_week_year = {'week' : datetime.date(calendar_year-1, 12, 28).isocalendar()[1], 'year':calendar_year-1} if calendar_week == 1 else {'week' : calendar_week-1, 'year':calendar_year}
	current_week_year = {'week' : week_now, 'day' : day_now, 'year' : year_now}


	context = {
		'dish_list_1st_breakfest' : dish_list_1st_breakfest,
		'dish_list_2nd_breakfest' : dish_list_2nd_breakfest,
		'dish_list_dinner' : dish_list_dinner,
		'dish_list_supper' : dish_list_supper,
		'next_week' : next_week_year,
		'previous_week' : previous_week_year,
		'current_week' : current_week_year,
		'week_dates' : dates
	}

	return render(request, 'calendar_plan.html', context=context)


def add_dish_to_calendarplan(request, day, month, year, meal_type, delete=0):

	if request.method == 'POST':
		form = CalendarPlanForm(request.POST, request.FILES)
		form.save()
		return HttpResponseRedirect(reverse('create_plan_calendar'))

	# Deleting meals from calendar with specified date and type
	if delete:
		CalendarPlan.objects.filter(meal_date=datetime.date(year=year, month=month, day=day), actual_type=meal_type).delete()

	form = CalendarPlanForm(initial = {'meal_date' : datetime.date(year=year, month=month, day=day), 'actual_type' : meal_type})
	form['meal_date'].disabled = True
	form['actual_type'].disabled = True

	# When adding meal for eg. breakfest there are only breakfests available on the list
	form.fields["dish_id"].queryset = Dish.objects.filter(meal_type=meal_type)

	context = {
		'form' : form,
	}

	# When not deleting object, move to adding meals to calendar page
	if not delete:
		return render(request, 'add_dish_to_calendarplan.html', context=context)
	# When deleting move back to calendar view
	else:
		return HttpResponseRedirect(reverse('create_plan_calendar'))


