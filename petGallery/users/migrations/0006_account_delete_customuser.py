# Generated by Django 5.0.3 on 2024-03-18 09:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Name')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='Username')),
                ('bio', models.CharField(blank=True, verbose_name='Bio')),
                ('age', models.IntegerField(verbose_name='Age')),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], max_length=20, verbose_name='Gender')),
                ('animal', models.CharField(choices=[('DOG', 'Dog'), ('CAT', 'Cat'), ('PARROT', 'Parrot'), ('OTHER', 'Other')], max_length=50, verbose_name='Animal')),
                ('breed', models.CharField(max_length=50, verbose_name='Breed')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Date Joined')),
                ('last_login', models.DateTimeField(default=datetime.datetime.now, verbose_name='Date Last log in')),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
