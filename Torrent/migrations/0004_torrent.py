# Generated by Django 4.1.2 on 2022-11-25 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Torrent", "0003_user_profile_pic"),
    ]

    operations = [
        migrations.CreateModel(
            name="torrent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=1000)),
                ("size", models.IntegerField()),
                ("downloads", models.IntegerField(default=0)),
                ("hash", models.CharField(max_length=40)),
                ("progress", models.FloatField(default=0)),
                (
                    "userid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Torrent.user"
                    ),
                ),
            ],
        ),
    ]
