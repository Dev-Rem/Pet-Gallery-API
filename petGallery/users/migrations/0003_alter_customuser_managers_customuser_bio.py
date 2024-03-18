# Generated by Django 5.0.3 on 2024-03-15 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.CharField(blank=True, verbose_name='Bio'),
        ),
    ]
