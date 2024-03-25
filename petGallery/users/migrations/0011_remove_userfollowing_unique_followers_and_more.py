# Generated by Django 5.0.3 on 2024-03-25 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_rename_follower_username_userfollowing_follower_id_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userfollowing',
            name='unique_followers',
        ),
        migrations.AddConstraint(
            model_name='userfollowing',
            constraint=models.UniqueConstraint(fields=('follower_id', 'following_id'), name='unique_followers'),
        ),
    ]