from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
# Register your models here.
from.models import (
    Client,
)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'tg_chat_id',
    )