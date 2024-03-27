# Generated by Django 5.0.3 on 2024-03-26 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_remove_followrequest_unique_follow_request_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='followaccount',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='blockaccount',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='followaccount',
            old_name='created',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='followrequest',
            name='request_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_follow_requests', to='users.account', verbose_name='From Account'),
        ),
        migrations.AlterField(
            model_name='followrequest',
            name='request_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_follow_requests', to='users.account', verbose_name='To Account'),
        ),
    ]