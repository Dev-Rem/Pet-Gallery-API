# Generated by Django 5.0.3 on 2024-03-25 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_userfollowing_unique_followers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfollowing',
            old_name='follower_username',
            new_name='follower_id',
        ),
        migrations.RenameField(
            model_name='userfollowing',
            old_name='following_username',
            new_name='following_id',
        ),
    ]
