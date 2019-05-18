# Generated by Django 2.1.1 on 2019-05-18 09:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('acronym', models.CharField(max_length=10, null=True)),
                ('image_file_path', models.FilePathField(null=True, path=None)),
                ('audio_file_path', models.FilePathField(null=True, path=None)),
            ],
        ),
        migrations.CreateModel(
            name='ChordIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Song.Chord')),
            ],
        ),
        migrations.CreateModel(
            name='IsFavourite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favourite', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sanskrit_name', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_pics')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('type', models.CharField(choices=[('KI', 'Kiirtan'), ('PS', 'Prabhat Samgiita'), ('BH', 'Bhajan')], max_length=30)),
                ('capo', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(12)])),
                ('description', models.TextField(blank=True)),
                ('written_by', models.CharField(blank=True, max_length=50)),
                ('song_text', models.TextField(blank=True)),
                ('audio_file', models.FileField(upload_to='')),
                ('upload_date', models.DateField(auto_now_add=True)),
                ('edit_date', models.DateField(auto_now=True)),
                ('chords', models.ManyToManyField(related_name='chords', through='Song.ChordIndex', to='Song.Chord')),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Song.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='liked_songs',
            field=models.ManyToManyField(related_name='liked_songs', through='Song.IsFavourite', to='Song.Song'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='isfavourite',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Song.Profile'),
        ),
        migrations.AddField(
            model_name='isfavourite',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Song.Song'),
        ),
        migrations.AddField(
            model_name='chordindex',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Song.Song'),
        ),
    ]
