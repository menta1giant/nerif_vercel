# Generated by Django 4.2.2 on 2023-07-06 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0007_endorsement_is_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='odds_change',
            field=models.FloatField(default=0.0),
        ),
    ]