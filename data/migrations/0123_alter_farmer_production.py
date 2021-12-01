# Generated by Django 3.2 on 2021-11-25 14:08

import data.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0122_alter_experiment_surface_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='production',
            field=data.forms.ChoiceArrayField(base_field=models.CharField(choices=[('Grandes cultures', 'Grandes cultures'), ('Cultures industrielles', 'Cultures industrielles'), ('Élevage allaitant', 'Élevage allaitant'), ('Élevage laitier', 'Élevage laitier'), ('Élevage engraissement', 'Élevage engraissement'), ('Élevage poule pondeuses', 'Élevage poule pondeuses'), ('Cultures légumières', 'Cultures légumières'), ('Vigne', 'Vigne'), ('Cultures spécialisées', 'Cultures spécialisées'), ('Apiculture', 'Apiculture'), ('Arboriculture', 'Arboriculture'), ('Autre', 'Autre')], max_length=100), blank=True, default=list, null=True, size=None),
        ),
    ]
