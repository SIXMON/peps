# Generated by Django 3.0.3 on 2020-04-20 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data', '0069_farmimage_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='external_id',
            field=models.CharField(db_index=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
