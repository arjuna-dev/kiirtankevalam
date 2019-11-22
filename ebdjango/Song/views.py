from django.shortcuts import render
from Song.models import Song, Profile, IsFavourite, Chord, ChordIndex
from Song.forms import UserForm, UserProfileInfoForm, SongForm, AddChordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
import json as simplejson
from django.middleware import csrf

allSongs     = Song.objects.all()
allKiirtan   = Song.objects.filter(type='KI')
allBhajan    = Song.objects.filter(type='BH')
allPs        = Song.objects.filter(type='PS')
allChords    = Chord.objects.all()

def lalita_view(request):
    return render(request,"lalita.html",{})

def song_view(request, songid): 
    song = allSongs.get(pk=songid)
    songChords = ChordIndex.objects.filter(song=song).values()
    return render(request, "song.html", {"song":song,"songChords":songChords,})

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
                                'allChords': allChords,
                                })

def togglefavoritesong_view(request):
    songId = request.GET.get('theId')
    previousPage = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        user = request.user.profile
        song = Song.objects.get(pk=songId)
        thisSongIsFavourite = IsFavourite.objects.filter(song=song, profile=user)
        if thisSongIsFavourite.exists():
            thisSongIsFavourite.delete()
        else:
            IsFavourite.objects.create(song=song, profile=user, is_favorite=True)
        context = {
            'song': song,
            'songId': songId,
        }
        if request.is_ajax():
            html = render_to_string('listitem.html', context, request=request)
            return JsonResponse({'form': html})

@login_required
def editchords_view(request):
    user             = request.user.profile
    lastSongByUser   = Song.objects.filter(uploader=user).last()
    lastSongChords   = ChordIndex.objects.filter(song=lastSongByUser)
    previousPage = request.META.get('HTTP_REFERER')
    return render(request,"editchords.html",
                                {
                                'songChords': lastSongChords,
                                'song': lastSongByUser,
                                'allChords':allChords,
                                })

def addchord_view(request, idChord):
    user                    = request.user.profile
    chord                   = Chord.objects.get(pk=idChord)
    print('chord')
    print(chord)
    songsByUser             = Song.objects.filter(uploader=user)
    lastSongByUser          = songsByUser.last()
    print('lastSongByUser')
    print(lastSongByUser)
    previousPage            = request.META.get('HTTP_REFERER')
    ChordIndex.objects.create(song=lastSongByUser, chord=chord)
    chordIndexCount = ChordIndex.objects.all().count()
    print("chordIndexCount")
    print(chordIndexCount)
    return HttpResponseRedirect(previousPage)

def deletechord_view(request):
    previousPage            = request.META.get('HTTP_REFERER')
    user                    = request.user.profile
    songsByUser             = Song.objects.filter(uploader=user)
    lastSongByUser          = songsByUser.last()
    lastChord               = ChordIndex.objects.filter(song=lastSongByUser).last()
    index                   = lastChord.id
    thisChord = ChordIndex.objects.filter(id=index)
    thisChord.delete()
    return HttpResponseRedirect(previousPage)


#_-_-_-_-_-_-_-_-_-_-_-_- Mainrenderer views _-_-_-_-_-_-_-_-_-_-_-_-_-_-

kiirtanContext = {
    'typeintitle': 'kiirtan',
    'kiirtanactive': 'active',
    'feedactive': 'active',
    'songlist': allKiirtan,
}

songtypecontext = {
    'kiirtanactive': 'active',
    'psactive': '',
    'bhajanactive': '',
}

def overtab_view(request):
    print(csrf.get_token(request))
    overtabData = request.GET.get('songType')
    print(overtabData)
    global songtypecontext
    listtypecontext = {
        'favactive': '',
        'feedactive': 'active',
        'allactive': '',
        'uploadsactive': '',
    }

    renderercontext = {
        'songlist': allKiirtan,
    }

    if overtabData == 'ki': 
        songtypecontext['kiirtanactive'] = 'active'
        songtypecontext['psactive']      = ''
        songtypecontext['bhajanactive']  = ''

        renderercontext = {
            'songlist': allKiirtan,
        }
    elif overtabData == 'ps': 
        songtypecontext['kiirtanactive'] = ''
        songtypecontext['psactive']      = 'active'
        songtypecontext['bhajanactive']  = ''
        renderercontext = {
            'songlist': allPs,
        }
    elif overtabData == 'bh': 
        songtypecontext['kiirtanactive'] = ''
        songtypecontext['psactive']      = ''
        songtypecontext['bhajanactive']  = 'active'
        renderercontext = {
            'songlist': allBhajan,
        }
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

def whichListType(listtypecontext):
    if listtypecontext['favactive'] == 'active':
        return 'fav'
    elif listtypecontext['feedactive'] == 'active':
        return 'feed'
    elif listtypecontext['allactive'] == 'active':
        return 'all'
    elif listtypecontext['uploadsactive'] == 'active':
        return 'up'

def undertab_view(request):
    undertabData = request.GET.get('listType')
    print(undertabData)
    global songtypecontext

    if request.user.is_authenticated:
        user        = request.user.profile
        upKiirtan   = allKiirtan.filter(uploader=user)
        upPs        = allPs.filter(uploader=user)
        upBhajan    = allBhajan.filter(uploader=user)
        favKiirtan  = user.liked_songs.all().filter(type="KI")
        favBhajan   = user.liked_songs.all().filter(type="BH")
        favPs       = user.liked_songs.all().filter(type="PS")
    else:
        upKiirtan   = None
        upPs        = None
        upBhajan    = None
        favKiirtan  = None
        favBhajan   = None
        favPs       = None

    if undertabData == 'fav': 
        listtypecontext = {
            'favactive': 'active',
            'feedactive': '',
            'allactive': '',
            'uploadsactive': '',
        }
    elif undertabData == 'feed':       
        listtypecontext = {
            'favactive': '',
            'feedactive': 'active',
            'allactive': '',
            'uploadsactive': '',
        }
    elif undertabData == 'all':        
        listtypecontext = {
            'favactive': '',
            'feedactive': '',
            'allactive': 'active',
            'uploadsactive': '',
        }
    elif undertabData == 'up':     
        listtypecontext = {
            'favactive': '',
            'feedactive': '',
            'allactive': '',
            'uploadsactive': 'active',
        }
    songtype = whichSongType(songtypecontext)
    listtype = whichListType(listtypecontext)

    songTypeDictionary =	{
        ("kiirtan", "fav"): { 'songlist': favKiirtan, 'type': "favorite"},
        ("kiirtan", "feed"): { 'songlist': allKiirtan},
        ("kiirtan", "all"): { 'songlist': allKiirtan},
        ("kiirtan", "up"): { 'songlist': upKiirtan, 'type': "uploads"},
        ("bhajan", "fav"): { 'songlist': favBhajan, 'type': "favorite"},
        ("bhajan", "feed"): { 'songlist': allBhajan},
        ("bhajan", "all"): { 'songlist': allBhajan},
        ("bhajan", "up"): { 'songlist': upBhajan, 'type': "uploads"},
        ("ps", "fav"): { 'songlist': favPs, 'type': "favorite"},
        ("ps", "feed"): { 'songlist': allPs},
        ("ps", "all"): { 'songlist': allPs},
        ("ps", "up"): { 'songlist': upPs, 'type': "uploads"},
    }

    for aTuple, aContext in songTypeDictionary.items():
        if aTuple == (songtype, listtype):
            renderercontext = aContext

    if request.is_ajax():
        html2 = render_to_string('undertabs.html', listtypecontext, request=request)
        html3 = render_to_string('renderer.html', renderercontext, request=request)
        json = simplejson.dumps({'undertabshtml': html2, 'songrendererhtml': html3})
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