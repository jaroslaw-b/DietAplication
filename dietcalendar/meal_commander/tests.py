from django.test import TestCase
from .models import CalendarPlan, Dish, Unit, Ingredient, DietIngredientQuantity
import datetime
# Create your tests here.

def add_meal_to_calendar_plan(_date, _type, _dish_id):

	return CalendarPlan.objects.create(meal_date=_date, actual_type=_type, dish_id=_dish_id)

class plan_calendarTest(TestCase):

	def setUp(self):
		for i in range(100):
			Dish.objects.create(name="meal_" + str(i), meal_type=i%4)

	'''
	Tests if request status code is correct for GET
	'''

	def test_no_meals(self):
		response = self.client.get('/plan_calendar/2020/1')

		self.assertEqual(response.status_code, 200)
	'''
	Test if series of meals are visible in dedicated weeks
	'''
	def test_meals_in_view(self):
		base = datetime.date(1994, 1, 4)
		date_list = [base + datetime.timedelta(days=x*7) for x in range(30)]
		dish = Dish.objects.filter(pk=1).values('name')
		for date in date_list:
			add_meal_to_calendar_plan(date, 1, _dish_id=Dish.objects.get(pk=1))
			year, week, day = date.isocalendar()
			with self.subTest():
				response = self.client.get('/plan_calendar/' + str(year) + '/' + str(week))
				self.assertEqual(response.status_code, 200)
				self.assertContains(response, dish[0]['name'])
	'''
	Test if series of meals are NOT visible in NOT dedicated weeks
	'''
	def test_meals_in_wrong_view(self):
		base = datetime.date(1994, 1, 4)
		date_list = [base + datetime.timedelta(days=7*x) for x in range(30)]
		dish = Dish.objects.filter(pk=1).values('name')
		for date in date_list:
			add_meal_to_calendar_plan(date, 1, _dish_id=Dish.objects.get(pk=1))
			year, week, day = date.isocalendar()
			with self.subTest():
				response = self.client.get('/plan_calendar/' + str(year) + '/' + str(week+1))
				self.assertEqual(response.status_code, 200)
				self.assertNotContains(response, dish[0]['name'])
	'''
	Test if four meals of four categories are placed in dedicated week
	'''
	def test_few_meals_in_week(self):
		date = datetime.date(2020, 2, 2)
		year, week, day = date.isocalendar()

		for i in range(1,4):
			add_meal_to_calendar_plan(date, i, _dish_id=Dish.objects.get(pk=i))
			dish = Dish.objects.filter(pk=i).values('name')
			with self.subTest():
				response = self.client.get('/plan_calendar/' + str(year) + '/' + str(week))
				self.assertEqual(response.status_code, 200)
				self.assertContains(response, dish[0]['name'])


class add_dish_to_calendarplanTest(TestCase):

	def setUp(self):
		for i in range(100):
			Dish.objects.create(name="meal_" + str(i), meal_type=i%4)

	def test_add_one_dish(self):
		self.client.post('/plan_calendar/add_dish/2020/1/1/0/', {'dish_id' : 1, 'meal_date' : datetime.date(2020,1,1), 'actual_type' : 0})
		response = self.client.get('/plan_calendar/2020/1')
		dish = Dish.objects.filter(pk=1).values('name')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, dish[0]['name'])

# Tests shopping list view
class shopping_listTest(TestCase):

	def setUp(self):
		Unit.objects.create(unit_type='g')
		Ingredient.objects.create(name='ing1', unit_id=Unit.objects.get(pk=1))
		Ingredient.objects.create(name='ing2', unit_id=Unit.objects.get(pk=1))
		Ingredient.objects.create(name='ing3', unit_id=Unit.objects.get(pk=1))
		Dish.objects.create(name='meal1', meal_type=1)
		DietIngredientQuantity.objects.create(dish_id=Dish.objects.get(pk=1), ingredient_id=Ingredient.objects.get(pk=1), quantity=10)
		DietIngredientQuantity.objects.create(dish_id=Dish.objects.get(pk=1), ingredient_id=Ingredient.objects.get(pk=2), quantity=20)
		DietIngredientQuantity.objects.create(dish_id=Dish.objects.get(pk=1), ingredient_id=Ingredient.objects.get(pk=3), quantity=30)
		CalendarPlan.objects.create(meal_date=datetime.date(2020, 2, 10), dish_id=Dish.objects.get(pk=1), actual_type=1)

# Message displayed if in provided period there's no meals
	def test_empty_shopping_list(self):

		response = self.client.get('/shopping_list')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'No meals in plan ;(')

# Checks if list of ingredients is present when there are some meals in provided period
	def test_shopping_list_with_one_meal(self):
		response = self.client.get('/shopping_list?date1=2020-02-06&date2=2020-02-13')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'ing1')
		self.assertContains(response, 'ing2')
		self.assertContains(response, 'ing3')
		self.assertContains(response, '10')
		self.assertContains(response, '20')
		self.assertContains(response, '30')
		self.assertNotContains(response, 'No meals in plan ;(')

# Check if list of ingredients is present when there are some meals in front edge of period
	def test_shopping_list_with_one_meal_edge(self):
		response = self.client.get('/shopping_list?date1=2020-02-10&date2=2020-02-13')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'ing1')
		self.assertContains(response, 'ing2')
		self.assertContains(response, 'ing3')
		self.assertContains(response, '10')
		self.assertContains(response, '20')
		self.assertContains(response, '30')
		self.assertNotContains(response, 'No meals in plan ;(')

# Check if list of ingredients is present when there are some meals in bottom edge of period
	def test_shopping_list_with_one_meal_edge2(self):
		response = self.client.get('/shopping_list?date1=2020-02-08&date2=2020-02-10')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'ing1')
		self.assertContains(response, 'ing2')
		self.assertContains(response, 'ing3')
		self.assertContains(response, '10')
		self.assertContains(response, '20')
		self.assertContains(response, '30')
		self.assertNotContains(response, 'No meals in plan ;(')

# Check if list of ingredients is correct for two meals
	def test_shopping_list_with_two_same_meals(self):
		CalendarPlan.objects.create(meal_date=datetime.date(2020, 2, 9), dish_id=Dish.objects.get(pk=1), actual_type=1)
		response = self.client.get('/shopping_list?date1=2020-02-08&date2=2020-02-10')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'ing1')
		self.assertContains(response, 'ing2')
		self.assertContains(response, 'ing3')
		self.assertContains(response, '20')
		self.assertContains(response, '40')
		self.assertContains(response, '60')
		self.assertNotContains(response, 'No meals in plan ;(')