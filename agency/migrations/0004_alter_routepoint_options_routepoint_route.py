# Generated by Django 4.0.3 on 2022-04-15 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0003_remove_route_comment_remove_route_count_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='routepoint',
            options={'verbose_name': 'Пункт маршрута', 'verbose_name_plural': 'Пункты маршрутов'},
        ),
        migrations.AddField(
            model_name='routepoint',
            name='route',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='agency.route', verbose_name='Маршрут'),
            preserve_default=False,
        ),
    ]
