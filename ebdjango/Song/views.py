import json as simplejson
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.middleware import csrf
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from .forms import SongForm, UserForm, UserProfileInfoForm
from .models import Chord, ChordIndex, IsFavourite, Profile, Song

def lalita_view(request):
    return render(request,"lalita.html",{})

def song_view(request, songid): 
    song = Song.objects.get(pk=songid)
    songChords = ChordIndex.objects.filter(song=song)
    return render(request, "song.html", {"song":song,"songChords":songChords})

@login_required
def createsong_view(request):
    previousPage   = request.META.get('HTTP_REFERER')
    user           = request.user.profile
    if request.method == 'POST':
        create_song_form  = SongForm(request.POST, request.FILES)
        if create_song_form.is_valid():
            newSong          = create_song_form.save()
            newSong.uploader = user
            newSong.save()
            return HttpResponseRedirect(reverse(editchords_view))
        else:
            return HttpResponseRedirect(previousPage)
    else:
        create_song_form = SongForm()
    return render(request,"createsong.html",
                                {'create_song_form':create_song_form,
                                'allChords': Chord.objects.all(),
                                })

def togglefavoritesong_view(request):
    songId  = request.GET.get('theId')
    song    = Song.objects.get(pk=songId)
    IsFavourite.manager.toggle_favorite(request, song)
    context = {
        'song': song,
        'songId': songId,
    }
    if request.is_ajax():
        html = render_to_string('listitem.html', context, request=request)
        return JsonResponse({'form': html})

@login_required
def editchords_view(request):
    lastSongByUser = Song.manager.get_last_song_by_user(request)
    lastSongChords   = ChordIndex.objects.filter(song=lastSongByUser)
    return render(
        request,
        "editchords.html",
        {
            'songChords': lastSongChords,
            'song': lastSongByUser,
            'allChords':Chord.objects.all(),
        })

def addchord_view(request, idChord):
    previousPage            = request.META.get('HTTP_REFERER')
    lastSongByUser          = Song.manager.get_last_song_by_user(request)
    chord                   = Chord.objects.get(pk=idChord)
    ChordIndex.objects.create(song=lastSongByUser, chord=chord)
    chordIndexCount         = ChordIndex.objects.all().count()
    return HttpResponseRedirect(previousPage)

def deletechord_view(request):
    previousPage            = request.META.get('HTTP_REFERER')
    lastSongByUser          = Song.manager.get_last_song_by_user(request)
    lastChord               = ChordIndex.objects.filter(song=lastSongByUser).last()
    lastChord.delete()
    return HttpResponseRedirect(previousPage)


#_-_-_-_-_-_-_-_-_-_-_-_- Mainrenderer views _-_-_-_-_-_-_-_-_-_-_-_-_-_-

kiirtanContext = {
    'typeintitle': 'kiirtan',
    'kiirtanactive': 'active',
    'feedactive': 'active',
    'songlist': Song.query.song_type('KI'),
}

songtypecontext = {
    'kiirtanactive': 'active',
    'psactive': '',
    'bhajanactive': '',
}

def overtab_view(request):
    overtabData = request.GET.get('songType')
    global songtypecontext

    listtypecontext = {'favactive': '','feedactive': 'active','allactive': '','uploadsactive': ''}

    renderercontext = {
        'songlist': Song.query.song_type('KI'),
    }

    songTypeDictionary = {
        'ki': ({'kiirtanactive': 'active','psactive': '','bhajanactive': ''}, {'songlist':Song.query.song_type('KI')}),
        'ps': ({'kiirtanactive': '','psactive': 'active','bhajanactive': ''}, {'songlist':Song.query.song_type('BH')}),
        'bh': ({'kiirtanactive': '','psactive': '','bhajanactive': 'active'}, {'songlist':Song.query.song_type('BH')})
    }

    for listType, theContext in songTypeDictionary.items():
        if listType == overtabData:
            songtypecontext = theContext[0]
            renderercontext = theContext[1]

    if request.is_ajax():
        html1 = render_to_string('overtabs.html', songtypecontext, request=request)
        html2 = render_to_string('undertabs.html', listtypecontext, request=request)
        html3 = render_to_string('renderer.html', renderercontext, request=request)
        json  = simplejson.dumps({'overtabshtml': html1, 'undertabshtml': html2, 'songrendererhtml': html3})
        return JsonResponse({'form': json})


def whichSongType(songtypecontext):
    if songtypecontext['kiirtanactive'] == 'active':
        return 'kiirtan'
    elif songtypecontext['psactive'] == 'active':
        return 'ps'
    elif songtypecontext['bhajanactive'] == 'active':
        return 'bhajan'

def undertab_view(request):
    undertabData = request.GET.get('listType')
    print(undertabData)
    global songtypecontext

    listTypeDictionary = {
        'fav': {'favactive': 'active','feedactive': '','allactive': '','uploadsactive': ''},
        'feed': {'favactive': '','feedactive': 'active','allactive': '','uploadsactive': ''},
        'all': {'favactive': '','feedactive': '','allactive': 'active','uploadsactive': ''},
        'up': {'favactive': '','feedactive': '','allactive': '','uploadsactive': 'active'}
    }

    for listType, theContext in listTypeDictionary.items():
        if listType == undertabData:
            listtypecontext = theContext

    songtype = whichSongType(songtypecontext)
    listtype = undertabData

    # if request.user.is_authenticated:
    user               = request.user.profile
    songTypeDictionary =	{
        ("kiirtan", "fav"): { 'songlist': user.liked_songs.all().filter(type="KI"), 'type': "favorite"},
        ("kiirtan", "feed"): { 'songlist': Song.query.song_type('KI')},
        ("kiirtan", "all"): { 'songlist': Song.query.song_type('KI')},
        ("kiirtan", "up"): { 'songlist': Song.query.song_type('KI').filter(uploader=user), 'type': "uploads"},
        ("bhajan", "fav"): { 'songlist': user.liked_songs.all().filter(type="BH"), 'type': "favorite"},
        ("bhajan", "feed"): { 'songlist': Song.query.song_type('BH')},
        ("bhajan", "all"): { 'songlist': Song.query.song_type('BH')},
        ("bhajan", "up"): { 'songlist': Song.query.song_type('BH').filter(uploader=user), 'type': "uploads"},
        ("ps", "fav"): { 'songlist': user.liked_songs.all().filter(type="PS"), 'type': "favorite"},
        ("ps", "feed"): { 'songlist': Song.query.song_type('PS')},
        ("ps", "all"): { 'songlist': Song.query.song_type('BH')},
        ("ps", "up"): { 'songlist': Song.query.song_type('BH').filter(uploader=user), 'type': "uploads"},
    }
    # else:
    #     songTypeDictionary =	{
    #         ("kiirtan", "fav"): { 'songlist': None, 'type': "favorite"},
    #         ("kiirtan", "feed"): { 'songlist': Song.query.song_type('KI')},
    #         ("kiirtan", "all"): { 'songlist': Song.query.song_type('KI')},
    #         ("kiirtan", "up"): { 'songlist': None, 'type': "uploads"},
    #         ("bhajan", "fav"): { 'songlist': None, 'type': "favorite"},
    #         ("bhajan", "feed"): { 'songlist': Song.query.song_type('BH')},
    #         ("bhajan", "all"): { 'songlist': Song.query.song_type('BH')},
    #         ("bhajan", "up"): { 'songlist': None, 'type': "uploads"},
    #         ("ps", "fav"): { 'songlist': None, 'type': "favorite"},
    #         ("ps", "feed"): { 'songlist': Song.query.song_type('BH')},
    #         ("ps", "all"): { 'songlist': Song.query.song_type('BH')},
    #         ("ps", "up"): { 'songlist': None, 'type': "uploads"},
    #     }

    for theTuple, theContext in songTypeDictionary.items():
        if theTuple == (songtype, listtype):
            renderercontext = theContext

    if request.is_ajax():
        undertabshtml = render_to_string('undertabs.html', listtypecontext, request=request)
        songrendererhtml = render_to_string('renderer.html', renderercontext, request=request)
        json = simplejson.dumps({'undertabshtml': undertabshtml, 'songrendererhtml': songrendererhtml})
        return JsonResponse({'form': json})


def mainrenderer_view(request):
    global kiirtanContext
    return render(request,"mainrenderer.html",kiirtanContext)


#_-_-_-_-_-_-_-_-_-_-_-_-Other views_-_-_-_-_-_-_-_-_-_-_-_-_-_-

def renderer_view(request):
    return render(request,"renderer.html",{})

def profile_view(request):
    return render(request,"profile.html",{})

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
            user = authenticate(
                username=user_form.cleaned_data['username'], 
                password=user_form.cleaned_data['password'],
            )
            login(request, user)
            return HttpResponseRedirect("/kiirtanfav/")
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'signup.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
