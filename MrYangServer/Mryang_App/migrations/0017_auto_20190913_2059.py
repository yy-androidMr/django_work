# Generated by Django 2.2 on 2019-09-13 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mryang_App', '0016_auto_20190913_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpath',
            name='dir',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dir_info', to='Mryang_App.Dir', unique=True),
        ),
    ]