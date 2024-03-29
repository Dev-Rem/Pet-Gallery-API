# Generated by Django 5.0.3 on 2024-03-25 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_userfollowing_unique_followers_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserFollowing',
            new_name='AccountFollowing',
        ),
        migrations.AlterField(
            model_name='accountfollowing',
            name='follower_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='users.account'),
        ),
        migrations.AlterField(
            model_name='accountfollowing',
            name='following_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='users.account'),
        ),
    ]
