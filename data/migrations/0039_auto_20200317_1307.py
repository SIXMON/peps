# Generated by Django 3.0.3 on 2020-03-17 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0038_auto_20200316_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='investment',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='surface_type',
            field=models.TextField(null=True),
        ),
    ]
