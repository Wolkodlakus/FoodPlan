from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Client(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Имя и фамилия клиента',
        blank=False,
        null=False,
    )
    tg_chat_id = models.PositiveIntegerField(
        verbose_name='Чат id клиента в Телеграм',
        unique=True,
        blank=False,
        null=False,
    )
    client_phonenumber = models.CharField(
        verbose_name='Номер клиента',
        max_length=20,
        blank=False,
        null=False,
        default='0'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Menu(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название Меню',
        blank=False,
        null=False,
    )
    def __str__(self):
        return f'{self.name}'
    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

class Allergy(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название аллергии',
        blank=False,
        null=False,
        default="Нет"
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Аллергия'
        verbose_name_plural = 'Аллергии'

class Subscription(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название подписки',
        blank=False,
        null=False,
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )
    portions = models.PositiveIntegerField(
        verbose_name='Количество порций',
        blank=False,
        null=False,
        default=1,
    )
    allergies = models.ManyToManyField(Allergy)
    created_at = models.DateTimeField(
        verbose_name='Когда создана подписка',
        default=timezone.now,
        blank=False,
        null=False,
    )
    period = models.IntegerField(
        verbose_name='Период подписки',
        blank=False,
        null=False,
        default=1,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

class Promo(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название промокода',
        blank=False,
        null=False,
    )
    code = models.CharField(
        max_length=256,
        verbose_name='Промокод',
        unique=True,
        blank=False,
        null=False,
    )
    valid_from = models.DateTimeField(
        verbose_name='С какой даты применим',
        default=timezone.now,
        blank=False,
        null=False,
    )
    valid_to = models.DateTimeField(
        verbose_name='По какую дату действует',
        default=timezone.now,
        blank=True,
        null=True,
    )
    discount = models.IntegerField(
        verbose_name='Размер скидки в процентах',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
    )
    active = models.BooleanField(
        verbose_name='Активность промокода',
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'