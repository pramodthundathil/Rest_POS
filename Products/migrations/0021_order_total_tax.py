# Generated by Django 5.0.6 on 2025-01-25 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0020_restaurantdetails_mobile_restaurantdetails_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_tax',
            field=models.FloatField(default=0),
        ),
    ]
