# Generated by Django 2.0 on 2018-05-28 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dir',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('isdir', models.BooleanField(default=True)),
                ('tags', models.CharField(default='', max_length=100)),
                ('abs_path', models.CharField(max_length=100)),
                ('rel_path', models.CharField(max_length=100)),
                ('type', models.IntegerField()),
                ('c_id', models.IntegerField(default=0)),
                ('show_level', models.IntegerField(default=0)),
                ('parent_dir', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='Mryang_App.Dir')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('token', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=100)),
                ('account', models.CharField(max_length=20)),
                ('pwd', models.CharField(max_length=200)),
                ('age', models.IntegerField(default=0)),
                ('regist_time', models.DateField(auto_now_add=True)),
                ('modify_time', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('video_path', models.FileField(null=True, upload_to='video/')),
                ('album_path', models.FileField(null=True, upload_to='album/')),
                ('upload_time', models.DateField(auto_now_add=True)),
                ('modify_time', models.DateField(auto_now=True)),
                ('user_token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mryang_App.User')),
            ],
        ),
    ]
