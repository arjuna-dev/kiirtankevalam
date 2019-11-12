from django.test import TestCase
from Song.models import Song, ChordIndex, IsFavourite, Profile, AlternateChordImage, Chord, Comment, ImageAsComment
from django.urls import reverse
from Song.forms import UserForm, UserProfileInfoForm, SongForm, AddChordForm
from django.contrib.auth.models import User


class TestModels(TestCase):

    def create_user(self, username, password):
        return User.objects.create(username=username, password=password)

    def test_user_creation(self):
        user = self.create_user("bobby", "password")
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

    def create_Chord(self):
        return Chord.objects.create(
            name            = "A minor",
            acronym         = "Am",
            image_file_path  = "a/file/path/chordy.jpg",
            audio_file       = None
        )
    
    def create_AlternateChordImage(self):
        chordy = self.create_Chord()
        return AlternateChordImage.objects.create(
            chord= chordy,
            image_file="chordy.jpg"
        )

    def test_AlternateChordImage_creation(self):
        chordImage = self.create_AlternateChordImage()
        self.assertTrue(isinstance(chordImage, AlternateChordImage))
    

    def create_profile(self, user, confirm_email, sanskrit_name, country, city, profile_pic):
        return Profile.objects.create(
            user             = user,
            confirm_email     = confirm_email,
            sanskrit_name    = sanskrit_name,
            country          = country,
            city             = city,
            profile_pic       = profile_pic
        )

    def test_Profile_creation(self):
        user = self.create_user("bobbo", "password")
        aProfile = self.create_profile(user, "asd@jdd.com", "Manju", "France", "Paris", "you.jpg")
        self.assertTrue(isinstance(aProfile, Profile))

    def create_comment(self):
        songy = self.create_song()
        user = self.create_user("bobbbo", "password")
        uploader = self.create_profile(user, "asd@jsdd.com", "Manju", "France", "Paris", "you.jpg")
        return Comment.objects.create(
            uploader  = uploader,
            song      = songy,
            comment   = "This is a test comment"
        )

    def test_comment_creation(self):
        commenty = self.create_comment()
        self.assertTrue(isinstance(commenty, Comment))

    def create_ImageAsComment(self):
        songy = self.create_song()
        user = self.create_user("tequila", "password")
        uploader = self.create_profile(user, "asd@jsdd.com", "Manju", "France", "Paris", "you.jpg")
        return ImageAsComment.objects.create(
            uploader   = uploader,
            song       = songy,
            image_file  = "file.jpg"
        )

    def test_ImageAsComment_creation(self):
        image = self.create_ImageAsComment()
        self.assertTrue(isinstance(image, ImageAsComment))


# class ImmageAsComment(models.Model):
#     uploader   = models.ForeignKey('Profile', null=True, on_delete=models.SET_NULL)
#     song       = models.ForeignKey('Song', null=True, on_delete=models.SET_NULL)
#     image_file  = models.ImageField(upload_to='alternate_chords/')
      

