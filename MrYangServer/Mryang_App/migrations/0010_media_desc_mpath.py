# Generated by Django 2.2 on 2019-10-02 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mryang_App', '0009_auto_20190930_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='desc_mpath',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='mulitPath', to='Mryang_App.MPath'),
        ),
    ]