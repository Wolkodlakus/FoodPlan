# Generated by Django 4.0.3 on 2022-03-31 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0003_client_subscriptions_alter_allergy_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allergy',
            options={'verbose_name': 'Аллергию', 'verbose_name_plural': 'Аллергии'},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Клиента', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'verbose_name': 'Подписку', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.RemoveField(
            model_name='client',
            name='subscriptions',
        ),
        migrations.AddField(
            model_name='client',
            name='subscriptions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodplan.subscription', verbose_name='Подписки'),
        ),
    ]
