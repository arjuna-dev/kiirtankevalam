from django.shortcuts import render
from Song.models import Song
from Song.models import Profile
from Song.models import IsFavourite
from Song.models import Chord
from Song.models import ChordProgression
from Song.forms import UserForm,UserProfileInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# import json
# from django.core import serializers

allSongs = Song.objects.all()

allKiirtan = Song.objects.filter(type='KI')
allBhajan = Song.objects.filter(type='BH')
allPS = Song.objects.filter(type='PS')

# Create your views here.

def main_view(request):
    return render(request,"base.html",{})
    
#_-_-_-_-_-_-_-_-_-_-_-_-Kiirtan views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Kiirtan views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Kiirtan views_-_-_-_-_-_-_-_-_-_-_-_-_-_-

def kiirtanfav_view(request):
    context = {
        'allKiirtan': allKiirtan,
        'typeintitle': 'kiirtan',
        'rendererview': renderer_view,
    }
    return render(request,"kiirtanfav.html",context)

def kiirtanall_view(request):
    context = {
        'allKiirtan': allKiirtan,
        'typeintitle': 'kiirtan',
    }
    return render(request,"kiirtanall.html",context)

def kiirtanfeed_view(request):
    context = {
        'allKiirtan': allKiirtan,
        'typeintitle': 'kiirtan',
        'allPS': allPS,
    }
    return render(request,"kiirtanfeed.html",context)

def kiirtanuploads_view(request):
    context = {
        'allKiirtan': allKiirtan,
        'typeintitle': 'kiirtan',
    }
    return render(request,"kiirtanuploads.html",context)

#_-_-_-_-_-_-_-_-_-_-_-_-PS views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-PS views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-PS views_-_-_-_-_-_-_-_-_-_-_-_-_-_-

def psfav_view(request):
    context = {
        'allPS': allPS,
        'typeintitle': 'ps',
    }
    return render(request,"psfav.html",context)

def psall_view(request):
    context = {
        'allPS': allPS,
        'typeintitle': 'ps',
    }
    return render(request,"psall.html",context)

def psfeed_view(request):
    context = {
        'allPS': allPS,
        'typeintitle': 'ps',
    }
    return render(request,"psfeed.html",context)

def psuploads_view(request):
    context = {
        'allPS': allPS,
        'typeintitle': 'ps',
    }
    return render(request,"psuploads.html",context)

#_-_-_-_-_-_-_-_-_-_-_-_-Bhajan views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Bhajan views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Bhajan views_-_-_-_-_-_-_-_-_-_-_-_-_-_-

def bhajanfav_view(request):
    context = {
        'allBhajan': allBhajan,
        'typeintitle': 'bhajan',
    }
    return render(request,"bhajanfav.html",context)

def bhajanall_view(request):
    context = {
        'allBhajan': allBhajan,
        'typeintitle': 'bhajan',
    }
    return render(request,"bhajanall.html",context)

def bhajanfeed_view(request):
    context = {
        'allBhajan': allBhajan,
        'typeintitle': 'bhajan',
    }
    return render(request,"bhajanfeed.html",context)

def bhajanuploads_view(request):
    context = {
        'allBhajan': allBhajan,
        'typeintitle': 'bhajan',
    }
    return render(request,"bhajanuploads.html",context)

#_-_-_-_-_-_-_-_-_-_-_-_-Other views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Other views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Other views_-_-_-_-_-_-_-_-_-_-_-_-_-_-

def renderer_view(request):
    context:{
        
    }
    return render(request,"renderer.html",context)

def song_view(request):
    return render(request,"song.html",{})

def record_view(request):
    return render(request,"record.html",{})

def newsong_view(request):
    return render(request,"newsong.html",{})

def profile_view(request):
    return render(request,"profile.html",{})

#_-_-_-_-_-_-_-_-_-_-_-_-Signup/Login Forms_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Signup/Login Forms_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Signup/Login Forms_-_-_-_-_-_-_-_-_-_-_-_-_-_-

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'signup.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})