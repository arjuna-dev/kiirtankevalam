# Generated by Django 2.1.1 on 2019-05-18 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Song', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chord',
            name='acronym',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chord',
            name='audio_file_path',
            field=models.FilePathField(default='', path=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chord',
            name='image_file_path',
            field=models.FilePathField(default='', path=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chord',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
