from django.shortcuts import render
from Song.models import Song, Profile, IsFavourite, Chord, ChordIndex
from Song.forms import UserForm, UserProfileInfoForm, SongForm, AddChordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string

from django.test import RequestFactory

from django.db import connection

allSongs    = Song.objects.all()
# allSongs    = Song.objects.raw('SELECT * FROM Song_Song')
allKiirtan  = Song.objects.filter(type='KI')
allBhajan   = Song.objects.filter(type='BH')
# allBhajan   = Song.objects.raw('SELECT * FROM Song_Song WHERE type="BH"')
allPs       = Song.objects.filter(type='PS')
allChords   = Chord.objects.all()


def song_view(request, songid): 
    song = allSongs.get(pk=songid)
    songChords = ChordIndex.objects.filter(song=song)
    return render(request, "song.html", {"song":song,"songChords":songChords,})

def createsong_view(request):
    previousPage   = request.META.get('HTTP_REFERER')
    user           = request.user.profile
    lastSongByUser = Song.objects.filter(uploader=user).last()
    if request.method == 'POST':
        create_song_form  = SongForm(request.POST, request.FILES)
        if create_song_form.is_valid():
            newSong          = create_song_form.save()
            newSong.uploader = user
            newSong.save()
            print("form is valid")
            return HttpResponseRedirect(reverse(editchords_view))
        else:
            print("form not valid")
            return HttpResponseRedirect(previousPage)
    else:
        create_song_form = SongForm()
    return render(request,"createsong.html",
                                {'create_song_form':create_song_form,
                                'allChords': allChords,
                                })

def addsong_view(request, id):
    previousPage = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        user = request.user.profile
        song = Song.objects.get(pk=id)
        IsFavourite.objects.create(song=song, profile=user, is_favorite=True)
        return HttpResponseRedirect(previousPage)
        # return HttpResponse(status=204)
    else:
        return HttpResponse(status=204)

def removesong_view(request, id):
    previousPage = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        user = request.user.profile
        song = Song.objects.get(pk=id)
        thisSong = IsFavourite.objects.filter(song=song, profile=user)
        thisSong.delete()
        return HttpResponseRedirect(previousPage)
        # return HttpResponse(status=204)
    else:
        return HttpResponse(status=204)


def addremovesong_view(request):
    songId = request.GET.get('theId')
    print(songId)
    isFavorite = False
    previousPage = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        user = request.user.profile
        song = Song.objects.get(pk=songId)
        thisSong = IsFavourite.objects.filter(song=song, profile=user)
        if thisSong.exists():
            thisSong.delete()
            isFavorite = False
        else:
            IsFavourite.objects.create(song=song, profile=user, is_favorite=True)
            isFavorite = True
        context = {
            'song': song,
            'songId': songId,
            'isFavorite': isFavorite,
        }
        if request.is_ajax():
            html = render_to_string('button.html', context, request=request)
            return JsonResponse({'form': html})
            
# def addremovesong_view(request):
#     songId = request.POST.get('theId')
#     print(songId)
#     isFavorite = False
#     previousPage = request.META.get('HTTP_REFERER')
#     if request.user.is_authenticated:
#         user = request.user.profile
#         song = Song.objects.get(pk=songId)
#         thisSong = IsFavourite.objects.filter(song=song, profile=user)
#         if thisSong.exists():
#             thisSong.delete()
#             isFavorite = False
#         else:
#             IsFavourite.objects.create(song=song, profile=user, is_favorite=True)
#             isFavorite = True
#         context = {
#             'song': song,
#             'songId': songId,
#             'isFavorite': isFavorite,
#         }
#         if request.is_ajax():
#             html = render_to_string('button.html', context, request=request)
#             return JsonResponse({'form': html})


@login_required
def editchords_view(request):
    user                    = request.user.profile
    lastSongByUser          = Song.objects.filter(uploader=user).last()
    songChords              = ChordIndex.objects.filter(song=lastSongByUser)
    # print('\n\n', connection.queries)
    # print('\n\n', songChords.query, '\n\n')
    # print(songChords.explain())
    previousPage = request.META.get('HTTP_REFERER')
    return render(request,"editchords.html",
                                {
                                'songChords': songChords,
                                'song': lastSongByUser,
                                'allChords':allChords,
                                })

def addchord_view(request, idChord):
    user                    = request.user.profile
    chord                   = Chord.objects.get(pk=idChord)
    songsByUser             = Song.objects.filter(uploader=user)
    lastSongByUser          = songsByUser.last()
    previousPage            = request.META.get('HTTP_REFERER')
    filterUserLastSong       = ChordIndex.objects.create(song=lastSongByUser, chord=chord)
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


#_-_-_-_-_-_-_-_-_-_-_-_-Kiirtan views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Kiirtan views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Kiirtan views_-_-_-_-_-_-_-_-_-_-_-_-_-_-

kiirtanContext = {
    'allKiirtan': allKiirtan,
    'typeintitle': 'kiirtan',
}

def kiirtanfav_view(request):
    if request.user.is_authenticated: 
        user = request.user
        kiirtanLikes = user.profile.liked_songs.all().filter(type="KI")
        global kiirtanContext
        kiirtanContext["kiirtanLikes"]=kiirtanLikes
        return render(request, "kiirtanfav.html", kiirtanContext)
    else:
        return render(request, "kiirtanfav.html", kiirtanContext)

def kiirtanall_view(request):
    global kiirtanContext
    return render(request,"kiirtanall.html",kiirtanContext)

def kiirtanfeed_view(request):
    global kiirtanContext
    return render(request,"kiirtanfeed.html",kiirtanContext)

def kiirtanuploads_view(request):
    if request.user.is_authenticated: 
        user = request.user.profile
        global kiirtanContext
        userUploads = allSongs.filter(uploader=user)
        kiirtanContext["userUploads"]=userUploads
        return render(request,"kiirtanuploads.html",kiirtanContext)
    else:
        return render(request,"kiirtanuploads.html",kiirtanContext)

#_-_-_-_-_-_-_-_-_-_-_-_-PS views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-PS views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-PS views_-_-_-_-_-_-_-_-_-_-_-_-_-_-

psContext = {
    'allPs': allPs,
    'typeintitle': 'P.S.',
}

def psfav_view(request):
    if request.user.is_authenticated:
        user = request.user
        psLikes = user.profile.liked_songs.all().filter(type="PS")
        global psContext
        psContext["psLikes"]=psLikes
        return render(request,"psfav.html",psContext)
    else:
        return render(request,"psfav.html",psContext)

def psall_view(request):
    global psContext
    return render(request,"psall.html",psContext)

def psfeed_view(request):
    global psContext
    return render(request,"psfeed.html",psContext)

def psuploads_view(request):
    global psContext
    return render(request,"psuploads.html",psContext)

#_-_-_-_-_-_-_-_-_-_-_-_-Bhajan views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Bhajan views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Bhajan views_-_-_-_-_-_-_-_-_-_-_-_-_-_-

bhajancontext = {
    'allBhajan': allBhajan,
    'typeintitle': 'bhajan',
}

def bhajanfav_view(request):
    if request.user.is_authenticated:
        user = request.user
        bhajanLikes = user.profile.liked_songs.all().filter(type="BH")
        global bhajancontext
        bhajancontext["bhajanLikes"]=bhajanLikes
        return render(request,"bhajanfav.html",bhajancontext)
    else:
        return render(request,"bhajanfav.html",bhajancontext)

def bhajanall_view(request):
    global bhajancontext
    return render(request,"bhajanall.html",bhajancontext)

def bhajanfeed_view(request):
    global bhajancontext
    return render(request,"bhajanfeed.html",bhajancontext)

def bhajanuploads_view(request):
    global bhajancontext
    return render(request,"bhajanuploads.html",bhajancontext)

#_-_-_-_-_-_-_-_-_-_-_-_-Other views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Other views_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#_-_-_-_-_-_-_-_-_-_-_-_-Other views_-_-_-_-_-_-_-_-_-_-_-_-_-_-

def renderer_view(request):
    return render(request,"renderer.html",{})

def record_view(request):
    return render(request,"record.html",{})

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

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request,user)
#                 return HttpResponseRedirect(reverse(kiirtanfav_view))
#             else:
#                 return HttpResponse("Your account was inactive.")
#         else:
#             print("Someone tried to login and failed.")
#             print("They used username: {} and password: {}".format(username,password))
#             return HttpResponse("Invalid login details given")
#     else:
#         return render(request, 'registration/login.html', {})

