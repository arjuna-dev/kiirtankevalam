from django import forms
from Song.models import Profile, Song, ChordIndex
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'password')

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = Profile
         fields = ('confirm_email', 'sanskrit_name', 'country', 'city', 'profile_pic')

class SongForm(forms.ModelForm):
    class Meta():
        model = Song
        fields = ('title', 'type', 'audio_file', 'description', 'written_by', 'song_text')

class AddChordForm(forms.ModelForm):
    class Meta():
        model = ChordIndex
        fields = ('chord', 'song')
