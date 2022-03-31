from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique category name')
        ]


class IngredientType(models.Model):
    name = models.CharField(max_length=200, default='Без категории')

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique ingredient type')
        ]


class Ingredient(models.Model):
    name = models.CharField(max_length=200, default='')
    type = models.ForeignKey(IngredientType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique ingredient name')
        ]


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    image_link = models.CharField(max_length=255, default='')
    categories = models.ManyToManyField(Category)
    person_nums = models.IntegerField(max_length=8)
    portions_count = models.IntegerField(max_length=8)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientsInfo')

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique recipe title')
        ]


class Step(models.Model):
    text = models.TextField(default='')
    number = models.IntegerField(max_length=4)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.recipe.title + ': Шаг - ' + str(self.number)


class IngredientsInfo(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    ingredient_amount = models.CharField(max_length=200)

    def __str__(self):
        return self.recipe.title + ' - ' + self.ingredient.name + ' - ' + self.ingredient_amount
