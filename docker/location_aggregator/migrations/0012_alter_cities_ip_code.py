# Generated by Django 3.2.3 on 2021-05-29 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location_aggregator', '0011_alter_cities_zip_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cities',
            name='ip_code',
            field=models.CharField(max_length=24, unique=True),
        ),
    ]
