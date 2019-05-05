# Generated by Django 2.2 on 2019-05-05 10:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Song', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='capo',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(12)]),
        ),
    ]
