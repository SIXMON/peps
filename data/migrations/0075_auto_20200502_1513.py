# Generated by Django 3.0.3 on 2020-05-02 15:13

import data.forms
from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0074_auto_20200502_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='tags',
            field=data.forms.ChoiceArrayField(base_field=models.CharField(choices=[('Maladies', 'Maladies'), ('Insectes et ravageurs', 'Insectes et ravageurs'), ('Adventices', 'Adventices'), ('Environnement & biodiversité', 'Environnement & biodiversité'), ('Diversification', 'Diversification'), ('Autonomie fourragère', 'Autonomie fourragère'), ('Productivité', 'Productivité'), ('Organisation du travail', 'Organisation du travail'), ('Réduction des charges', 'Réduction des charges'), ('Autre', 'Autre')], max_length=255), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='agriculture_types',
            field=data.forms.ChoiceArrayField(base_field=models.TextField(choices=[('Agriculture Biologique', 'Agriculture Biologique'), ('Agriculture de Conservation des Sols', 'Agriculture de Conservation des Sols'), ('Techniques Culturales Simplifiées', 'Techniques Culturales Simplifiées'), ('Labour occasionnel', 'Labour occasionnel'), ('Agroforesterie', 'Agroforesterie'), ('Conventionnel', 'Conventionnel'), ('Cahier des charges industriel', 'Cahier des charges industriel'), ('Label qualité', 'Label qualité'), ('Autre', 'Autre')]), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='cultures',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='groups',
            field=data.forms.ChoiceArrayField(base_field=models.CharField(choices=[('DEPHY', 'DEPHY'), ('GIEE', 'GIEE'), ('30000', '30000'), ('CETA', 'CETA'), ('Groupe de coopérative', 'Groupe de coopérative'), ('Groupe de négoce', 'Groupe de négoce'), ("Groupe de chambre d'agriculture", "Groupe de chambre d'agriculture"), ('Groupe de voisins', 'Groupe de voisins'), ('CUMA', 'CUMA'), ('Autre', 'Autre')], max_length=200), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='installation_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='links',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='livestock_number',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='livestock_type',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='output',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='personnel',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='production',
            field=data.forms.ChoiceArrayField(base_field=models.CharField(choices=[('Grandes cultures', 'Grandes cultures'), ('Cultures industrielles', 'Cultures industrielles'), ('Élevage allaitant', 'Élevage allaitant'), ('Élevage laitier', 'Élevage laitier'), ('Élevage engraissement', 'Élevage engraissement'), ('Élevage poule pondeuses', 'Élevage poule pondeuses'), ('Cultures légumières', 'Cultures légumières'), ('Vigne', 'Vigne'), ('Autre', 'Autre')], max_length=100), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='soil_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='specificities',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='surface',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='surface_cultures',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='surface_meadows',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmimage',
            name='label',
            field=models.TextField(blank=True, null=True),
        ),
    ]
