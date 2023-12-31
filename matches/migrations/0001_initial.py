# Generated by Django 4.2.2 on 2023-07-05 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('match_id', models.IntegerField(primary_key=True, serialize=False)),
                ('match_date', models.DateTimeField(auto_now_add=True)),
                ('odds_favorite', models.FloatField(default=2.0)),
                ('odds_opponent', models.FloatField(default=2.0)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UpcomingCoeff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('odds', models.FloatField(default=0.0)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('match', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='matches.match')),
            ],
        ),
        migrations.CreateModel(
            name='PredictedMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map_order', models.IntegerField(default=1)),
                ('date_predicted', models.DateTimeField(auto_now_add=True)),
                ('pick_category', models.IntegerField(default=0)),
                ('match', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='matches.match')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='team_favorite',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='team_favorite', to='matches.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_opponent',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='team_opponent', to='matches.team'),
        ),
    ]
