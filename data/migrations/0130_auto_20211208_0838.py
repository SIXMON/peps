# Generated by Django 3.2 on 2021-12-08 08:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0129_auto_20211202_0842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='ir_done',
        ),
        migrations.AddField(
            model_name='experiment',
            name='ir_score',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
