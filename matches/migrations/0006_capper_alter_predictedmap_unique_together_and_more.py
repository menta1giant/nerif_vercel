# Generated by Django 4.2.2 on 2023-07-06 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0005_alter_predictedmap_ruleset_favorite_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('link', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='predictedmap',
            unique_together={('match', 'map_order')},
        ),
        migrations.CreateModel(
            name='Endorsement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='matches.capper')),
                ('related_map', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='matches.predictedmap')),
            ],
        ),
    ]
