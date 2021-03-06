# Generated by Django 2.2 on 2019-10-04 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mryang_App', '0015_media_audio_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='src_dir',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='srcDir', to='Mryang_App.Dir'),
        ),
        migrations.AlterField(
            model_name='mpath',
            name='drive_memory_mb',
            field=models.IntegerField(default=24576, verbose_name='磁盘剩余空间小于此数值时,不选择此路径'),
        ),
    ]
