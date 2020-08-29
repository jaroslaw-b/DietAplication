from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dish', views.dish, name='dish'),
    path('ingredient', views.ingredient, name='ingredient'),
    path('ingredient/<int:ingredient_id>', views.ingredient_detail, name='ingredient_detail'),
    path('units/<int:unit_id>', views.unit_detail, name='unit_detail'),
    path('dish/<dish_name>', views.dish_detail, name='dish_detail'),
    path('plan/<int:plan_id>', views.plan_detail, name='plan_detail'),
    path('add_dish_details/<dish_name>', views.add_dish_details, name='add_dish_details'),
    path('add_ingredient', views.add_ingredient, name='add_ingredient'),
    path('add_dish/<int:meal_type>', views.add_dish, name='add_dish'),
    path('create_plan', views.create_plan, name='create_plan'),
    path('create_plan/<int:day>/<int:meal_type>', views.create_plan, name='create_plan'),
    path('create_plan/<int:day>/<int:meal_type>/<int:delete>', views.create_plan, name='create_plan'),
    path('create_plan_calendar/<int:calendar_year>/<int:calendar_week>', views.create_plan_calendar, name='create_plan_calendar'),
    path('create_plan_calendar/', views.create_plan_calendar, name='create_plan_calendar'),
    path('create_plan_calendar/add_dish_to_calendarplan/<int:year>/<int:month>/<int:day>/<int:meal_type>/', views.add_dish_to_calendarplan, name='add_dish_to_calendarplan'),
    path('create_plan_calendar/add_dish_to_calendarplan/<int:year>/<int:month>/<int:day>/<int:meal_type>/<int:delete>', views.add_dish_to_calendarplan, name='add_dish_to_calendarplan')
]