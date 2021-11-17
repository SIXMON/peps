# Generated by Django 3.2 on 2021-11-16 15:43

import data.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0117_auto_20210928_0742'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='workshop',
            field=models.TextField(blank=True, choices=[('Grandes cultures', 'Grandes cultures'), ("Cultures d'industrie", "Cultures d'industrie"), ('Productions légumières de plein champ', 'Productions légumières de plein champ'), ('Elevage ruminant', 'Elevage ruminant'), ('Elevage monogastrique', 'Elevage monogastrique'), ('Arboriculture', 'Arboriculture'), ('Viticulture', 'Viticulture'), ('Maraîchage diversifié', 'Maraîchage diversifié'), ('PPAM', 'PPAM'), ('Cultures spécialisées', 'Cultures spécialisées')]),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='xp_type',
            field=models.TextField(blank=True, choices=[("Maîtrisée & intégrée en routine à l'exploitation", "Maîtrisée & intégrée en routine à l'exploitation"), ("Prometteuse & en cours d'amélioration pour être maîtrisée", "Prometteuse & en cours d'amélioration pour être maîtrisée"), ('Un premier essai, à renouveler pour mieux juger de son potentiel', 'Un premier essai, à renouveler pour mieux juger de son potentiel'), ('Abandonnée car non satisfaisante', 'Abandonnée car non satisfaisante')], null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='agriculture_types',
            field=data.forms.ChoiceArrayField(base_field=models.TextField(choices=[('Agriculture Biologique', 'Agriculture Biologique'), ('Agriculture de Conservation des Sols', 'Agriculture de Conservation des Sols'), ('Techniques Culturales Simplifiées', 'Techniques Culturales Simplifiées'), ('Labour occasionnel', 'Labour occasionnel'), ('Agroforesterie', 'Agroforesterie'), ('Arboriculture', 'Arboriculture'), ('Conventionnel', 'Conventionnel'), ('Cahier des charges industriel', 'Cahier des charges industriel'), ('Label qualité', 'Label qualité'), ('Label environnemental (HVE)', 'Label environnemental (HVE)'), ('Autre', 'Autre')]), blank=True, default=list, null=True, size=None),
        ),
    ]
