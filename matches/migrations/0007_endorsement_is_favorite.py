# Generated by Django 4.2.2 on 2023-07-06 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0006_capper_alter_predictedmap_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='endorsement',
            name='is_favorite',
            field=models.BooleanField(default=True),
        ),
    ]
