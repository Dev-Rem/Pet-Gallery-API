# Generated by Django 5.0.3 on 2024-03-25 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_account_private_account_userfollowing_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfollowing',
            old_name='user_id',
            new_name='follower_username',
        ),
        migrations.RenameField(
            model_name='userfollowing',
            old_name='following_user_id',
            new_name='following_username',
        ),
    ]