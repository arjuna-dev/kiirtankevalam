from django.db import models

# Create your models here.

class Song(models.Model):
    title          = models.CharField(max_length=120)
    SONG_TYPES     = (
        ('KI', 'Kiirtan'),
        ('PS', 'Prabhat Samgiita'),
        ('BH', 'Bhajan'),
    )
    type           = models.CharField(max_length=30, choices=SONG_TYPES)
    capo           = models.PositiveIntegerField(blank=True, null=True)
    description    = models.TextField(blank=True)
    uploader       = models.ForeignKey('User', null=True, on_delete=models.SET_NULL)
    written_by     = models.CharField(max_length=50, blank=True)      
    song_text      = models.TextField(blank=True)
    audio_file_path = models.FilePathField(path=None, match=None, max_length=100)
    upload_date    = models.DateField(auto_now=False, auto_now_add=True)
    edit_date      = models.DateField(auto_now=True, auto_now_add=False)

class User(models.Model):
    name          = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    sanskrit_name = models.CharField(max_length=100, blank=True, null=True)
    email         = models.CharField(max_length=100, unique=True)
    password      = models.CharField(max_length=25)
    sign_up_date  = models.DateField(auto_now=False, auto_now_add=True)
    edit_date     = models.DateField(auto_now=True, auto_now_add=False)
    country       = models.CharField(max_length=50)
    city          = models.CharField(max_length=50, blank=True, null=True)
    photo         = models.FilePathField(path=None, match=None, max_length=100, null=True)
    liked_songs   = models.ManyToManyField(Song, through='IsFavourite')

class IsFavourite(models.Model):
    song         = models.ForeignKey(Song, on_delete=models.CASCADE)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    is_favourite = models.BooleanField()

class Chord(models.Model):
    name            = models.CharField(max_length=100)
    acronym         = models.CharField(max_length=10)
    image_file_path  = models.FilePathField(path=None, match=None, max_length=100)
    audio_file_path  = models.FilePathField(path=None, match=None, max_length=100)

class ChordProgression(models.Model):
    chord = models.ManyToManyField(Chord)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)