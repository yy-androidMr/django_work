# Generated by Django 2.2 on 2019-07-03 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mryang_App', '0008_auto_20190703_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='picinfo',
            name='src_md5',
            field=models.CharField(default='', max_length=50),
        ),
    ]