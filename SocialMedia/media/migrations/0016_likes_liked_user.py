# Generated by Django 4.2.6 on 2024-03-06 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("media", "0015_remove_posts_dislikes_remove_posts_likes_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="likes",
            name="liked_user",
            field=models.ManyToManyField(
                default=None, null=True, related_name="userlikedPosts", to="media.posts"
            ),
        ),
    ]
