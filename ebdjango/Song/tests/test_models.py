from django.test import TestCase, Client
from Song.models import Song, ChordIndex, Chord, IsFavourite, Profile
from django.urls import reverse
from Song.views import addchord_view
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from Song.views import profile_view, song_view, createsong_view, editchords_view, addsong_view

class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        # self.addsong_url = reverse(addsong_view)
        self.createsong_url = reverse(createsong_view)

    # POST Method
    def test_create_song_view_POST(self):
        testUser = User.objects.create(username='testuser')
        testUser.set_password('12345')
        testUser.save()
        testProfile = Profile.objects.create(
            user=testUser,
            sanskrit_name = "Shanti",
            country       = "Mexico"
        )
        testProfile.save()
        logged_in = self.client.login(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        audio = SimpleUploadedFile("103_VASANTA_AJ_JAGALO_04Tsyry.mp3", b"file_content", content_type="audio/mp3")

        response = self.client.post(self.createsong_url, {'title': 'Hello', 'type': 'KI', 'audio_file': audio})

        self.assertTrue(Song.objects.filter(title='Hello').exists()) 
      

    # def test_add_chord(self):
    #     response = self.client.get(self.addchord_url)
