# Generated by Django 5.0.3 on 2024-03-25 12:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_accountblocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountblocked',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_users', to='users.account'),
        ),
    ]
