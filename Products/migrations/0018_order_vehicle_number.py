# Generated by Django 5.0.6 on 2024-06-24 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0017_orderitem_add_ons'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='vehicle_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
