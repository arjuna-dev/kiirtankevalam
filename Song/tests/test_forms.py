from django.test import TestCase, Client
from Song.forms import SongForm, UserForm
from Song.models import Song
from django.contrib.auth.models import User
from Song.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_Song_form_is_valid(self):
        upload_file = open('103_VASANTA_AJ_JAGALO_04Tsyry.mp3', 'rb')
        theFile = {'audio_file': SimpleUploadedFile(upload_file.name, upload_file.read())}
        the_data = {
          'title': 'Hello',
          'type': 'KI',
        }
        form = SongForm(the_data, theFile)
        self.assertTrue(form.is_valid())

    def test_Song_form_is_not_valid(self):
        the_data = {
          'title': 'Hello',
          'type': 'KI',
        }
        form = SongForm(the_data)
        self.assertFalse(form.is_valid())

    def test_user_form_is_valid(self):
        the_data = {
          'username': 'hotPotato',
          'password': 'asd123asd'
        }
        form = UserForm(data=the_data)
        self.assertTrue(form.is_valid())

    def test_user_form_is_not_valid(self):
        the_data = {
          'username': 'hot',
          'password': 'asd'
        }
        form = UserForm(data=the_data)
        self.assertTrue(form.is_valid())
