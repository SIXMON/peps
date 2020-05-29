# Generated by Django 3.0.3 on 2020-05-27 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0081_remove_farmer_livestock_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='lon',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
