# Generated by Django 5.0.7 on 2024-08-30 08:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sequence_memory", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="gamescoresequencememory",
            name="date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
