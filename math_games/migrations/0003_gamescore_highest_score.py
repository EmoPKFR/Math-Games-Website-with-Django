# Generated by Django 5.0.7 on 2024-08-07 20:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("math_games", "0002_alter_gamelevel_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="gamescore",
            name="highest_score",
            field=models.IntegerField(default=0),
        ),
    ]