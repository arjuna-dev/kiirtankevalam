import sys
sys.path.append("..")
from django.shortcuts import render
from Song.models import Song
from Song.models import User
from Song.models import IsFavourite
from Song.models import Chord
from Song.models import ChordProgression
# import json
# from django.core import serializers

allSongs = Song.objects.all()

allKiirtan = Song.objects.filter(type='KI')
allKiirtan = Song.objects.filter(type='KI').filter()

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

