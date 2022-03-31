from django.contrib import admin

from .models import Category, Ingredient, Recipe, IngredientsInfo, Step

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(IngredientsInfo)
admin.site.register(Step)
