# Generated by Django 4.0.3 on 2022-04-01 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0006_category_ingredient_ingredientsinfo_ingredienttype_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название блюда')),
                ('portions', models.PositiveIntegerField(default=1, verbose_name='Количество порций')),
                ('ingredients', models.TextField(verbose_name='Ингридиенты')),
                ('recipe', models.TextField(verbose_name='Рецепт')),
                ('allergies', models.ManyToManyField(to='foodplan.allergy', verbose_name='Аллергии')),
                ('menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodplan.menu')),
            ],
        ),
    ]
