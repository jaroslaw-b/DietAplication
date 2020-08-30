from django.test import TestCase
from .models import CalendarPlan, Dish, Unit
import datetime
# Create your tests here.

def add_meal_to_calendar_plan(_date, _type, _dish_id):

	return CalendarPlan.objects.create(meal_date=_date, actual_type=_type, dish_id=_dish_id)

class create_plan_calendarTest(TestCase):

	def setUp(self):
		for i in range(100):
			Dish.objects.create(name="meal_" + str(i), meal_type=i%4)

	'''
	Tests if request status code is correct for GET
	'''

	def test_no_meals(self):
		response = self.client.get('/create_plan_calendar/2020/1')

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
				response = self.client.get('/create_plan_calendar/' + str(year) + '/' + str(week))
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
				response = self.client.get('/create_plan_calendar/' + str(year) + '/' + str(week+1))
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
				response = self.client.get('/create_plan_calendar/' + str(year) + '/' + str(week))
				self.assertEqual(response.status_code, 200)
				self.assertContains(response, dish[0]['name'])
