# Generated by Django 2.2 on 2019-09-15 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mryang_App', '0022_auto_20190915_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryinfo',
            name='src_real_path',
            field=models.CharField(default='', max_length=500),
        ),
    ]