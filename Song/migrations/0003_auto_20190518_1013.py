# Generated by Django 2.1.1 on 2019-05-18 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Song', '0002_auto_20190518_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chord',
            name='audio_file_path',
        ),
        migrations.AlterField(
            model_name='chord',
            name='image_file_path',
            field=models.FilePathField(path='static/resources/img/chords'),
        ),
    ]
