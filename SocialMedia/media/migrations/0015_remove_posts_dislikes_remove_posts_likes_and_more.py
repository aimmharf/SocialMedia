# Generated by Django 4.2.6 on 2024-03-06 19:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("media", "0014_likes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="posts",
            name="dislikes",
        ),
        migrations.RemoveField(
            model_name="posts",
            name="likes",
        ),
        migrations.AddField(
            model_name="posts",
            name="liked_users",
            field=models.ManyToManyField(
                default=None,
                null=True,
                related_name="UserLiked",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
