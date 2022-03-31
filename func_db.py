import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adminka_foodplan.settings")
django.setup()

from foodplan.models import Allergy, Client, Menu, Promo, Subscription

def find_client(chat_id):
    """Функция возвращает id клиента по его id в телеграмме. Либо None"""
    try:
        client = Client.objects.filter(tg_chat_id=chat_id)
    except Client.DoesNotExist:
        return None
    return client.id


def add_client(chat_id, name, phonenumber):
    """Функция добавляет нового клиента"""
    Client.objects.create(
        name = name,
        tg_chat_id = chat_id,
        client_phonenumber = phonenumber,
    )

def add_subscription():
    pass

def get_client_subscriptions(id_client):
    try:
        client = Client.objects.filter(id=id_client)
    except Client.DoesNotExist:
        return None
    subscriptions = client.subscriptions
    pass

def get_dish():
    pass


def get_allergies():
    """Функция выводит список аллергий"""
    allergies = []
    for item in Allergy.objects.all():
        allergies.append(item.name)
    return allergies

if __name__== '__main__':
    pass
