from django.test import TestCase, Client
from django.urls import reverse
from Song.views import profile_view, song_view, createsong_view, editchords_view, addsong_view
from Song.models import Song, Profile, ChordIndex, Chord, IsFavourite
import json
import requests
from django.contrib.auth.models import User
from Song.forms import SongForm

# song = Song(title="songy", pk=10000, type="KI", upload_date="1923-08-23")
# song.save()


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.profile_url = reverse(profile_view)
        # self.addsong_url = reverse(addsong_view)
        self.song_url = reverse(song_view, args=['1001'])
        self.createsong_url = reverse(createsong_view)
        self.editchords_url = reverse(editchords_view)
        self.Song = Song
        self.songy = Song.objects.create(
            id=1001,
            title="songy", 
            type="KI",
            upload_date="1923-08-23",
            audio_file = "103_VASANTA_AJ_JAGALO_04Tsyry.mp3"
        )

    def test_profile_view_GET(self):
        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_song_view_GET(self):
        response = self.client.get(self.song_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'song.html')

    # def test_addsong_view_GET(self):
    #     response = self.client.get(self.addsong_url)
    #     self.assertEquals(response.status_code, 200)

    def test_createsong_view_GET_not_logged_in(self):
        response = self.client.get(self.createsong_url)
        self.assertEquals(response.status_code, 302)

    def test_createsong_view_GET(self):
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
        response = self.client.get(self.createsong_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'createsong.html')

    # POST Method

    # def test_create_song_view_POST(self):
    #     testUser = User.objects.create(username='testuser')
    #     testUser.set_password('12345')
    #     testUser.save()
    #     testProfile = Profile.objects.create(
    #         user=testUser,
    #         sanskrit_name = "Shanti",
    #         country       = "Mexico"
    #     )
    #     testProfile.save()
    #     # logged_in = self.client.login(username='testuser', password='12345')
    #     self.client.login(username='testuser', password='12345')
    #     # response = self.client.get(self.createsong_url)
    #     response = self.client.post(self.createsong_url, {
    #         'title': 'song34', 
    #         'type': 'KI', 
    #         'description': '', 
    #         'written_by': '', 
    #         'song_text': '', 
    #         # 'create_song_form': 'Create Song'
    #     })
    #     # self.assertTrue(testUser.is_authenticated)
    #     self.assertTrue(Song.objects.filter(title='song34').exists()) 
    #     # self.assertEquals(response.status_code, 200)
    #     # self.assertEquals(self.Song.objects.last().title, "song34")


    # def test_create_song_view_POST_no_data(self):
    #     response = self.client.post(self.createsong_url)
    #     self.assertEquals(response.status_code, 302)
    #     self.assertEquals(Song.objects.all().count, 1)


    #Logged in

    def test_logged_in(self):
        testUser = User.objects.create(username='testuser')
        testUser.set_password('12345')
        testUser.save()
        logged_in = self.client.login(username='testuser', password='12345')
        testProfile = Profile.objects.create(
            user=testUser,
            sanskrit_name = "Shanti",
            country       = "Mexico"
        )
        testProfile.save()
        
        self.assertEquals(User.objects.last().username, 'testuser')
        self.assertTrue(testUser.is_authenticated)