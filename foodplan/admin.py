from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
# Register your models here.
from.models import (
    Client,
    Menu,
    Subscription,
    Allergy,
    Promo,
)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'tg_chat_id',
    )

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'code',
        'valid_from',
        'valid_to',
        'discount',
        'active'
    )

@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name',
    )

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'name', 'menu',
        'portions',
        'created_at', 'period',
    )
