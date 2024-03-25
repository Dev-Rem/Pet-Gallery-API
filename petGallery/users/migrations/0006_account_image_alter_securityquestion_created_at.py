# Generated by Django 5.0.3 on 2024-03-21 10:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_securityquestion_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='image',
            field=models.ImageField(default='default.png', upload_to='profile_photos', verbose_name='Profile photo'),
        ),
        migrations.AlterField(
            model_name='securityquestion',
            name='created_at',
            field=models.DateField(default=datetime.date.today, verbose_name='Date created'),
        ),
    ]