# Generated by Django 5.0.3 on 2024-03-30 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashtag',
            name='created_at',
        ),
    ]