from django.test import TestCase
from Song.models import Song, ChordIndex, IsFavourite, Profile, AlternateChordImage, Chord
from django.urls import reverse
from Song.forms import UserForm, UserProfileInfoForm, SongForm, AddChordForm
from django.contrib.auth.models import User


class TestModels(TestCase):

    def create_user(self, username="bobby103", password="Passw0rd"):
        return User.objects.create(username=username, password=password)

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, User))

    def create_song(self):
        return Song.objects.create(
            id=100100,
            title="songy", 
            type="KI",
            upload_date="1923-08-23",
            audio_file = "103_VASANTA_AJ_JAGALO_04Tsyry.mp3"
        )

    def test_song_creation(self):
        song = self.create_song()
        self.assertTrue(isinstance(song, Song))
    
    def create_AlternateChordImage(self):
        chordy = Chord.objects.create(
            name            = "A minor",
            acronym         = "Am",
            image_file_path  = "a/file/path/chordy.jpg",
            audio_file       = None
        )
        return AlternateChordImage.objects.create(
            chord= chordy,
            image_file="chordy.jpg"
        )

    def test_AlternateChordImage_creation(self):
        chordImage = self.create_AlternateChordImage()
        self.assertTrue(isinstance(chordImage, AlternateChordImage))
      

