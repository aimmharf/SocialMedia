# Generated by Django 4.2.6 on 2024-03-03 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("media", "0010_rename_one_being_followed_follow_user_being_followed_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Likes",
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
                (
                    "dislikes",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dislikeUser",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "likes",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likeUser",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
