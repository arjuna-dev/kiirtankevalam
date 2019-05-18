from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator

# Create your models here.

class Song(models.Model):
    title          = models.CharField(max_length=120)
    SONG_TYPES     = (
        ('KI', 'Kiirtan'),
        ('PS', 'Prabhat Samgiita'),
        ('BH', 'Bhajan'),
    )
    type              = models.CharField(max_length=30, choices=SONG_TYPES)
    capo              = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(12)])
    description       = models.TextField(blank=True)
    uploader          = models.ForeignKey('Profile', null=True, on_delete=models.SET_NULL)
    written_by        = models.CharField(max_length=50, blank=True)      
    song_text         = models.TextField(blank=True)
    audio_file         = models.FileField()
    upload_date       = models.DateField(auto_now=False, auto_now_add=True)
    edit_date         = models.DateField(auto_now=True, auto_now_add=False)
    chords            = models.ManyToManyField('Chord', related_name='chords', through='ChordIndex')
    

class Profile(models.Model):
    user          = models.OneToOneField(User,on_delete=models.CASCADE)
    sanskrit_name = models.CharField(max_length=100)
    country       = CountryField(max_length=50)
    city          = models.CharField(max_length=50, blank=True, null=True)
    profile_pic    = models.ImageField(upload_to='profile_pics',blank=True)
    liked_songs   = models.ManyToManyField(Song, related_name="liked_songs", through='IsFavourite')
    def __str__(self):
        return self.user.username

class IsFavourite(models.Model):
    song         = models.ForeignKey(Song, on_delete=models.CASCADE)
    profile       = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_favorite  = models.BooleanField(default=True)

class Chord(models.Model):
    name            = models.CharField(max_length=100)
    acronym         = models.CharField(max_length=10)
    image_file_path  = models.FilePathField(path='static/resources/img/chords', match=None, max_length=100)
    # audio_file_path  = models.FilePathField(path=None, match=None, max_length=100)

class ChordIndex(models.Model):
    chord  = models.ForeignKey('Chord', on_delete=models.CASCADE)
    song   = models.ForeignKey('Song', on_delete=models.CASCADE)