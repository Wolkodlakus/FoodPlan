from django.db import models

# Create your models here.

class Client(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name='Имя и фамилия клиента'
    )
    tg_chat_id = models.PositiveIntegerField(
        verbose_name='Чат id клиента в Телеграм',
        unique=True
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'