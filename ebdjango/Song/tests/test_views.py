import json
import time
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from Song.forms import SongForm
from Song.models import Chord, ChordIndex, IsFavourite, Profile, Song
from Song.views import (createsong_view, editchords_view, profile_view, signup,
                        song_view)


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

    def login(self):
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
        return testUser
        
    def test_editchords_view_GET(self):
        self.login()
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
        self.login()
        response = self.client.get(self.createsong_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'createsong.html')

    #Logged in

    def test_logged_in(self):
        testUser = self.login()
        self.assertEquals(User.objects.last().username, 'testuser')
        self.assertTrue(testUser.is_authenticated)

    # POST Method
    def test_create_song_view_POST(self):
        self.login()
        audio = SimpleUploadedFile("103_VASANTA_AJ_JAGALO_04Tsyry.mp3", b"file_content", content_type="audio/mp3")
        response = self.client.post(self.createsong_url, {'title': 'Hello', 'type': 'KI', 'audio_file': audio})
        self.assertTrue(Song.objects.filter(title='Hello').exists()) 

# With Selenium

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class TestSignup(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path='/Users/i5/Documents/Documents/Docs/CODE/2ndSemester/Kiirtan-Kevalam/kiirtanenv/geckodriver')
        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # options.add_argument('window-size=1200x600')
        # self.driver = webdriver.Chrome(chrome_options=options)

    def test_click_favorite_not_logged_in(self):
        self.driver.get("http://localhost:8000/")
        self.driver.find_element_by_class_name('pratik').click()
        time.sleep(0.03)
        self.assertTrue(self.driver.find_element_by_id('alerto').is_displayed())

    # def test_kiirtan_are_rendered(self):
    #     self.driver.get("http://localhost:8000/")
    #     overtabs             = self.driver.find_elements_by_class_name('overtab')
    #     undertabs            = self.driver.find_elements_by_class_name('undertab')
    #     rendered_songs       = self.driver.find_elements_by_class_name('favBtn')
    #     songtype_dict        = {}
    #     listtype_dict        = {}
    #     rendered_songs_list  = []

    #     for element in overtabs:
    #         songtype_dict[element.get_attribute('data-songtype')] = element
            
    #     for element in undertabs:
    #         listtype_dict[element.get_attribute('data-listtype')] = element

    #     for element in rendered_songs:
    #         rendered_songs_list.append(element.get_attribute('data-pid'))

    #     songtype_dict['bh'].click()
    #     print(rendered_songs_list)
    #     print(rendered_songs_list[3])
    #     song = Song.objects.get(pk=rendered_songs_list[3])
        


    def tearDown(self):
        self.driver.quit

if __name__ == '__main__':
    unittest.main()
