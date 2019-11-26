from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django_countries.fields import CountryField

class QueryManager(models.Manager):
    def song_type(self, song_type):
        if song_type == 'KI':
            return super().get_queryset().filter(type='KI')
        elif song_type == 'PS':
            return super().get_queryset().filter(type='PS')
        elif song_type == 'BH':
            return super().get_queryset().filter(type='BH')

class SongManager(models.Manager):
    def get_last_song_by_user(self, request):
        user             = request.user.profile
        lastSongByUser   = Song.objects.filter(uploader=user).last()
        return lastSongByUser

class Song(models.Model):
    SONG_TYPES     = (
        ('KI', 'Kiirtan'),
        ('PS', 'Prabhat Samgiita'),
        ('BH', 'Bhajan'),
    )
    type           = models.CharField(max_length=30, choices=SONG_TYPES)
    title          = models.CharField(max_length=120)
    capo           = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(12)])
    description    = models.TextField(blank=True)
    uploader       = models.ForeignKey('Profile', null=True, on_delete=models.SET_NULL)
    written_by     = models.CharField(max_length=50, blank=True)      
    song_text      = models.TextField(blank=True)
    audio_file      = models.FileField(upload_to='songs/')
    upload_date    = models.DateField(auto_now=False, auto_now_add=True)
    edit_date      = models.DateField(auto_now=True, auto_now_add=False)
    chords         = models.ManyToManyField('Chord', related_name='chords', through='ChordIndex')

    objects        = models.Manager()
    manager        = SongManager()
    query          = QueryManager()
    
class Profile(models.Model):
    user             = models.OneToOneField(User,on_delete=models.CASCADE)
    confirm_email     = models.EmailField()
    sanskrit_name    = models.CharField(max_length=100)
    country          = CountryField(max_length=50)
    city             = models.CharField(max_length=50, blank=True, null=True)
    profile_pic       = models.ImageField(upload_to='profile_pics/', blank=True)
    liked_songs      = models.ManyToManyField(Song, related_name="liked_songs", through='IsFavourite')
    gold_member      = models.BooleanField(default=False, null=True, blank=True)
    platinum_member  = models.BooleanField(default=False, null=True, blank=True)
    admin_member     = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self):
        return self.user.username

class FavoriteManager(models.Manager):
    def create_favorite(self, song, profile, is_favorite):
        favorite = self.create(song=song, profile=profile, is_favorite=is_favorite)
        return favorite

    def get_favorite(self, song, profile):
        get_favorite = super().get_queryset().filter(song=song, profile=profile)
        return get_favorite

    def check_if_favorite(self, aFavorite):
        isFavorite  = aFavorite.exists()
        return isFavorite

    def toggle_favorite(self, request, song):
        if request.user.is_authenticated:
            profile        = request.user.profile
            aFavorite     = IsFavourite.manager.get_favorite(song=song, profile=profile)
            isFavorite    = IsFavourite.manager.check_if_favorite(aFavorite)
            if isFavorite:
                aFavorite.delete()
            else:
                IsFavourite.manager.create_favorite(song, profile, True)

class IsFavourite(models.Model):
    song         = models.ForeignKey(Song, on_delete=models.CASCADE)
    profile       = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_favorite  = models.BooleanField(default=True)

    objects      = models.Manager()
    manager      = FavoriteManager()

class Chord(models.Model):
    name            = models.CharField(max_length=100)
    acronym         = models.CharField(max_length=10)
    image_file_path  = models.FilePathField(path='static/resources/img/chords', match=None, max_length=100)
    audio_file       = models.FileField(upload_to='chords/', null=True, blank=True)

class AlternateChordImage(models.Model):
    chord      = models.ForeignKey('Chord', on_delete=models.CASCADE)
    image_file  = models.ImageField(upload_to='alternate_chords/')

class ChordIndex(models.Model):
    chord  = models.ForeignKey('Chord', on_delete=models.CASCADE)
    song   = models.ForeignKey('Song', on_delete=models.CASCADE)

class Comment(models.Model):
    uploader  = models.ForeignKey('Profile', null=True, on_delete=models.SET_NULL)
    song      = models.ForeignKey('Song', null=True, on_delete=models.SET_NULL)
    comment   = models.TextField()

class ImageAsComment(models.Model):
    uploader   = models.ForeignKey('Profile', null=True, on_delete=models.SET_NULL)
    song       = models.ForeignKey('Song', null=True, on_delete=models.SET_NULL)
    image_file  = models.ImageField(upload_to='alternate_chords/')
