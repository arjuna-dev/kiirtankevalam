from django.test import TestCase, Client
from django.urls import reverse
from Song.views import profile_view, song_view, createsong_view, editchords_view, signup
from Song.models import Song, Profile, ChordIndex, Chord, IsFavourite
import json
from django.contrib.auth.models import User
from Song.forms import SongForm
from django.core.files.uploadedfile import SimpleUploadedFile
import time

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.profile_url = reverse(profile_view)
        self.createsong_url = reverse(createsong_view)
        self.editchords_url = reverse(editchords_view)
        self.signup_url = reverse(signup)
        self.Song = Song

    def test_signup_view_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_profile_view_GET(self):
        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_editchords_view_GET(self):
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
        response = self.client.get(self.editchords_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'editchords.html')

    def test_editchords_view_GET_not_logged_in(self):
        response = self.client.get(self.editchords_url)
        self.assertEquals(response.status_code, 302)

    def test_song_view_GET(self):
        self.song_url = reverse(song_view, args=['100100'])
        self.songy = Song.objects.create(
            id=100100,
            title="songy", 
            type="KI",
            upload_date="1923-08-23",
            audio_file = "103_VASANTA_AJ_JAGALO_04Tsyry.mp3"
        )
        response = self.client.get(self.song_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'song.html')

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

# # With Selenium

# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# class TestSignup(unittest.TestCase):

#     def setUp(self):
#         # self.driver = webdriver.Firefox(executable_path='/Users/i5/Documents/Documents/Docs/CODE/2ndSemester/Kiirtan-Kevalam/kiirtanenv/geckodriver')
#         options = webdriver.ChromeOptions()
#         options.add_argument('headless')
#         options.add_argument('window-size=1200x600')
#         self.driver = webdriver.Chrome(chrome_options=options)


#     def test_click_favorite_not_logged_in(self):
#         self.driver.get("http://localhost:8000/")
#         self.driver.find_element_by_class_name('pratik').click()
#         time.sleep(0.03)
#         self.assertTrue(self.driver.find_element_by_id('alerto').is_displayed())

#     def test_homepage_is_rendered(self):
#         self.driver.get("http://localhost:8000/")

#     def tearDown(self):
#         self.driver.quit

# if __name__ == '__main__':
#     unittest.main()