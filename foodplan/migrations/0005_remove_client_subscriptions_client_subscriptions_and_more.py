# Generated by Django 4.0.3 on 2022-03-31 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0004_alter_allergy_options_alter_client_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='subscriptions',
        ),
        migrations.AddField(
            model_name='client',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, null=True, to='foodplan.subscription', verbose_name='Подписки'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='allergies',
            field=models.ManyToManyField(to='foodplan.allergy', verbose_name='Аллергии'),
        ),
    ]