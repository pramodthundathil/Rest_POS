# Generated by Django 5.0.6 on 2024-06-21 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0016_addons'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='add_ons',
            field=models.ManyToManyField(blank=True, null=True, to='Products.addons'),
        ),
    ]
