# Generated by Django 4.2.6 on 2024-04-06 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("media", "0024_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="first_name",
            field=models.CharField(max_length=100000),
        ),
        migrations.AlterField(
            model_name="profile",
            name="last_name",
            field=models.CharField(max_length=100000),
        ),
        migrations.AlterField(
            model_name="profile",
            name="username",
            field=models.CharField(max_length=100000),
        ),
    ]
