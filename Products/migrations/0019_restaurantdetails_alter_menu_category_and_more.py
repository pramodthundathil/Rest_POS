# Generated by Django 5.0.6 on 2025-01-25 05:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0018_order_vehicle_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name_of_restaurant', models.CharField(max_length=255)),
                ('TRN', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=255)),
                ('Address', models.CharField(max_length=255)),
                ('logo', models.FileField(blank=True, null=True, upload_to='logo')),
            ],
        ),
        migrations.AlterField(
            model_name='menu',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.foodcategory'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='potion',
            field=models.CharField(choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], max_length=255),
        ),
    ]
