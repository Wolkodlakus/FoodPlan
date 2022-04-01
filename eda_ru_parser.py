from requests_html import HTMLSession
from django.http import HttpResponse
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adminka_foodplan.settings")
django.setup()

from foodplan.models import Category, Ingredient, Recipe, IngredientsInfo, IngredientType, Step

max_pages = 50
base_url = 'https://eda.ru'
menu_categories = {
    'Вегетерианское меню': 'recepty/vegetarianskaya-eda',
    'Низкоуглеводная еда': '/recepty/nizkokaloriynaya-eda',
    'Классическое меню': '/recepty/osnovnye-blyuda'
}


def get_recipes(category_url, max_pages):
    recipes = []
    for page_num in range(1, max_pages + 1):
        url = f'{base_url}/{category_url}?page={page_num}'
        session = HTMLSession()
        response = session.get(url)
        images_links = [img.attrs['src'] for img in response.html.find('.emotion-10j91xu')]
        recipes_links = [link.attrs['href'] for link in response.html.find('.emotion-12sjte8')]
        recipes = dict(zip(recipes_links, images_links))

    return recipes


def get_recipe(url):
    session = HTMLSession()
    response = session.get(url)
    title = response.html.find('h1', first=True).text
    portions_count = response.html.find('.emotion-1047m5l', first=True).text
    ingredients_names = [element.text for element in response.html.find('.emotion-1g8buaa span')]
    ingredients_count = [element.text for element in response.html.find('.emotion-15im4d2')]
    ingredients = dict(zip(ingredients_names, ingredients_count))
    steps = [element.text for element in response.html.find('.emotion-6kiu05 span')]
    return {
        'title': title,
        'portions_count': portions_count,
        'ingredients': ingredients,
        'steps': steps
    }


def start_parser(request):
    for category_name, category_url in menu_categories.items():
        # Сохраняем категорию рецепта в бд
        category, cat_created = Category.objects.get_or_create(name=category_name)
        recipes = get_recipes(category_url, max_pages)
        for recipe_url, recipe_img in recipes.items():
            url = f'{base_url}{recipe_url}'
            recipe = get_recipe(url)
            recipe_model, recipe_model_created = Recipe.objects.get_or_create(
                title=recipe['title'],
                image_link=recipe_img,
                person_nums=recipe['portions_count'],
                portions_count=recipe['portions_count']
            )
            recipe_model.categories.add(category)
            # Сохраняем ингредиенты в бд
            for name, amount in recipe['ingredients'].items():
                ingredient_type, ingredient_type_created = IngredientType.objects.get_or_create(name='Нет категории')
                ingredient, ingredient_created = Ingredient.objects.get_or_create(name=name, type=ingredient_type)
                recipe_model.ingredients.add(
                    ingredient,
                    through_defaults={
                        'ingredient_amount': amount
                    }
                )
                recipe_model.save()
            for count, value in enumerate(recipe['steps'], start=1):
                step = Step(number=count, text=value, recipe_id=recipe_model.id)
                step.save()
                recipe_model.step_set.add(step)
                recipe_model.save()

    return HttpResponse('Done!')
