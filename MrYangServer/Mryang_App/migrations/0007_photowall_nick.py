# Generated by Django 2.2 on 2019-09-22 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mryang_App', '0006_photo_photo_wall'),
    ]

    operations = [
        migrations.AddField(
            model_name='photowall',
            name='nick',
            field=models.CharField(default='', max_length=100),
        ),
    ]
