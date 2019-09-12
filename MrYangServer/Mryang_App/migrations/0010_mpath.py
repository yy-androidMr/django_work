# Generated by Django 2.2 on 2019-09-12 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mryang_App', '0009_picinfo_src_md5'),
    ]

    operations = [
        migrations.CreateModel(
            name='MPath',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('path', models.CharField(default='', max_length=500, unique=True)),
                ('type', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('drive_memory_mb', models.IntegerField(default=0)),
                ('param1', models.CharField(default='', max_length=500)),
                ('param2', models.CharField(default='', max_length=500)),
            ],
        ),
    ]
