from django.contrib import admin

# Register your models here.

from .models import Unit, Ingredient, Dish, DietIngredientQuantity, CalendarPlan

admin.site.register(Unit)
admin.site.register(Ingredient)
admin.site.register(Dish)
admin.site.register(DietIngredientQuantity)
admin.site.register(CalendarPlan)