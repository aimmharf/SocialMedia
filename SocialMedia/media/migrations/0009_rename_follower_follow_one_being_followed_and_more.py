# Generated by Django 4.2.6 on 2024-03-03 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("media", "0008_remove_follow_follower_follow_follower"),
    ]

    operations = [
        migrations.RenameField(
            model_name="follow",
            old_name="follower",
            new_name="one_being_followed",
        ),
        migrations.RenameField(
            model_name="follow",
            old_name="user",
            new_name="one_that_is_following",
        ),
    ]
