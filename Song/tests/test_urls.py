from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Song.views import editchords_view,  mainrenderer_view, lalita_view, overtab_view, undertab_view, createsong_view


class TestUrls(SimpleTestCase):

    def test_edit_chords_url_is_resolved(self):
        url = reverse('edit-chords-view')
        self.assertEquals(resolve(url).func, editchords_view)

    def test_overtab_view_url_is_resolved(self):
        url = reverse('overtab-view')
        self.assertEquals(resolve(url).func, overtab_view)

    def test_undertab_view_url_is_resolved(self):
        url = reverse('undertab-view')
        self.assertEquals(resolve(url).func, undertab_view)

    def test_create_song_view_url_is_resolved(self):
        url = reverse('create-song-view')
        self.assertEquals(resolve(url).func, createsong_view)
