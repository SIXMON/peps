# Generated by Django 3.2 on 2021-11-30 15:04

import data.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0125_alter_experiment_workshop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='workshop',
            field=models.TextField(blank=True, choices=[('Grandes cultures', 'Grandes cultures'), ("Cultures d'industries", "Cultures d'industries"), ('Légumes de plein champs', 'Légumes de plein champs'), ('Élevage ruminant', 'Élevage ruminant'), ('Élevage monogastrique', 'Élevage monogastrique'), ('Arboriculture', 'Arboriculture'), ('Viticulture', 'Viticulture'), ('Maraîchage diversifié', 'Maraîchage diversifié'), ('Apiculture', 'Apiculture'), ('PPAM', 'PPAM'), ('Cultures spécialisées', 'Cultures spécialisées')], null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='production',
            field=data.forms.ChoiceArrayField(base_field=models.CharField(choices=[('Grandes cultures', 'Grandes cultures'), ("Cultures d'industries", "Cultures d'industries"), ('Légumes de plein champs', 'Légumes de plein champs'), ('Élevage ruminant', 'Élevage ruminant'), ('Élevage monogastrique', 'Élevage monogastrique'), ('Arboriculture', 'Arboriculture'), ('Viticulture', 'Viticulture'), ('Maraîchage diversifié', 'Maraîchage diversifié'), ('Apiculture', 'Apiculture'), ('PPAM', 'PPAM'), ('Cultures spécialisées', 'Cultures spécialisées')], max_length=100), blank=True, default=list, null=True, size=None),
        ),
    ]
