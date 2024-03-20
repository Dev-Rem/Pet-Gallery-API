# Generated by Django 5.0.3 on 2024-03-19 16:00

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_account_date_joined_remove_account_last_login_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=150, verbose_name='Question')),
                ('answer', models.CharField(max_length=150, verbose_name='Answer')),
                ('created_at', models.DateField(default=datetime.datetime.now, verbose_name='Date created')),
                ('last_used', models.DateTimeField(default=datetime.datetime.now, verbose_name='Date last used')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]