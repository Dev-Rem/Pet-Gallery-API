# Generated by Django 5.0.3 on 2024-05-05 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_alter_comment_liked_by_alter_comment_post_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_date',
            new_name='date_commented',
        ),
    ]
