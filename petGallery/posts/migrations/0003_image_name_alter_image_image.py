# Generated by Django 5.0.3 on 2024-04-26 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_remove_hashtag_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(null=True, verbose_name='File name'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default=None, upload_to='post_images/', verbose_name='Image'),
            preserve_default=False,
        ),
    ]
