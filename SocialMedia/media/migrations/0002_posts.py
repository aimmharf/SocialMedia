# Generated by Django 4.2.6 on 2024-02-24 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("media", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Posts",
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
                ("first_name", models.CharField(max_length=1000)),
                ("last_name", models.CharField(max_length=1000)),
                ("username", models.CharField(max_length=1000)),
                ("date", models.DateTimeField()),
                ("post", models.TextField()),
            ],
        ),
    ]
