from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dish', views.dish, name='dish'),
    path('ingredient', views.ingredient, name='ingredient'),
    path('ingredient/<int:ingredient_id>', views.ingredient_detail, name='ingredient_detail'),
    path('units/<int:unit_id>', views.unit_detail, name='unit_detail'),
    path('dish/<dish_name>', views.dish_detail, name='dish_detail'),
    path('add_dish_details/<dish_name>', views.add_dish_details, name='add_dish_details'),
    path('add_ingredient', views.add_ingredient, name='add_ingredient'),
    path('add_dish/<int:meal_type>', views.add_dish, name='add_dish'),
    path('delete_dish/<dish_name>', views.delete_dish, name='delete_dish'),
    path('plan_calendar/<int:calendar_year>/<int:calendar_week>', views.plan_calendar, name='plan_calendar'),
    path('plan_calendar/', views.plan_calendar, name='plan_calendar'),
    path('plan_calendar/add_dish/<int:year>/<int:month>/<int:day>/<int:meal_type>/', views.add_dish_to_calendarplan, name='add_dish_to_calendarplan'),
    path('plan_calendar/add_dish/<int:year>/<int:month>/<int:day>/<int:meal_type>/<int:delete>', views.add_dish_to_calendarplan, name='add_dish_to_calendarplan'),
    path('shopping_list', views.shopping_list, name='shopping_list')
]