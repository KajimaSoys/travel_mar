# Generated by Django 4.0.3 on 2022-04-16 18:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0006_remove_route_clients_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
    ]