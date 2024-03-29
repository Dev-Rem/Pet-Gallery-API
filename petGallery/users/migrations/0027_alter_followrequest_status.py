# Generated by Django 5.0.3 on 2024-03-27 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_alter_followrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followrequest',
            name='status',
            field=models.CharField(choices=[('ACCEPTED', 'Accepted'), ('DECLINED', 'Declined'), ('PENDING', 'Pending')], default='PENDING', verbose_name='Request status'),
        ),
    ]
