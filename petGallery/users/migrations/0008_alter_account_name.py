# Generated by Django 5.0.3 on 2024-03-18 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_account_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Name'),
        ),
    ]
