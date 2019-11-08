from django.test import TestCase, Client
from Song.models import Song, ChordIndex, Chord, IsFavourite, Profile
from django.urls import reverse
from Song.views import addchord_view

# class TestModels(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.addchord_url = reverse(addchord_view)
        # self.song1 = Song.objects.create(
        #     id=1001,
        #     title="songy", 
        #     type="KI",
        #     upload_date="1923-08-23",
        #     audio_file = "103_VASANTA_AJ_JAGALO_04Tsyry.mp3"            
        # )

    # def test_add_chord(self):
    #     response = self.client.get(self.addchord_url)
