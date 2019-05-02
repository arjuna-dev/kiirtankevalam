from django import forms
from Song.models import Profile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'password')

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = Profile
         fields = ('sanskrit_name', 'country', 'city', 'profile_pic')
