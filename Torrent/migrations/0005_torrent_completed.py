# Generated by Django 4.1.2 on 2022-12-04 04:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Torrent", "0004_torrent"),
    ]

    operations = [
        migrations.AddField(
            model_name="torrent",
            name="completed",
            field=models.BooleanField(default=False),
        ),
    ]
