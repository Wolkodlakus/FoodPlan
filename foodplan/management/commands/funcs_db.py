import os

import django
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adminka_foodplan.settings")
django.setup()

from foodplan.models import Allergy, Client, Menu, Subscription


def find_client(chat_id):
    """Функция возвращает id клиента по его id в телеграмме. Либо None"""
    try:
        client = Client.objects.get(tg_chat_id=chat_id)
    except Client.DoesNotExist:
        return None
    print(client)
    print(type(client))
    return client.id


def add_client(chat_id, name, phonenumber):
    """Функция добавляет нового клиента"""
    Client.objects.create(
        name=name,
        tg_chat_id=chat_id,
        client_phonenumber=phonenumber,
    )


def add_subscription(id_client, menu_id, portions, period, allergy):
    num = len(get_client_subscriptions(id_client))
    subscription = Subscription.objects.create(
        name=f'{num + 1} подписка',
        menu=Menu.objects.get(id=menu_id),
        portions=portions,
        created_at=timezone.now(),
        period=period,
        client = Client.objects.get(id=id_client),

    )
    #На случай нескольких аллергий
    #for item in allergies_id:
    #    subscription.allergies.add(get_allergy(item))
    #Client.objects.get(id=id_client).subscriptions.add(subscription)
    # если передаём только одну аллергию
    allergies = get_allergy2(allergy)
    subscription.allergies.add(allergies)

    return subscription.id

def get_allergy2(allergy_name):
    return Allergy.objects.get(name=allergy_name)

def get_allergy(allergy_id):
    return Allergy.objects.get(id=allergy_id)


def get_client_subscriptions(id_client):
    try:
        client = Client.objects.get(id=id_client)
    except Client.DoesNotExist:
        return None
    return client.subscriptions.all()


def get_allergies():
    """Функция выводит список аллергий"""
    allergies = []
    for item in Allergy.objects.all():
        allergies.append(item.name)
    return allergies


if __name__ == '__main__':
    pass
