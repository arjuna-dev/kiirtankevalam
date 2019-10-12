"""kiirtankevalam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from django.urls import path, include
#For serving media:
from django.conf import settings
from django.conf.urls.static import static

from Song.views import record_view, song_view, profile_view, kiirtanfav_view, kiirtanall_view, kiirtanuploads_view, kiirtanfeed_view, psfav_view, psall_view, psuploads_view, psfeed_view, bhajanfav_view, bhajanall_view, bhajanuploads_view, bhajanfeed_view, signup, addsong_view, removesong_view, deletechord_view, createsong_view, editchords_view, addchord_view, togglefavoritesong_view, lalita_view

urlpatterns = [
    path('', kiirtanfeed_view),
    path('lalita/', lalita_view),
    path('kiirtanfav/', kiirtanfav_view),
    path('kiirtanfeed/', kiirtanfeed_view),
    path('kiirtanall/', kiirtanall_view),
    path('kiirtanuploads/', kiirtanuploads_view),
    path('psfav/', psfav_view),
    path('psfeed/', psfeed_view),
    path('psall/', psall_view),
    path('psuploads/', psuploads_view),
    path('bhajanfav/', bhajanfav_view, name='bhajan-fav-view'),
    path('bhajanfeed/', bhajanfeed_view),
    path('bhajanall/', bhajanall_view),
    path('bhajanuploads/', bhajanuploads_view),
    path('song/<int:songid>', song_view, name='song-view'),
    path('record/', record_view),
    path('createsong/', createsong_view, name='create-song-view'),
    path('editchords/', editchords_view, name='edit-chords-view'),
    path('profile/', profile_view),
    path('signup/', signup, name='signup'),
    # path('login/', user_login, name='user_login'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('addsongview/<int:id>', addsong_view, name='add-song-view'),
    path('removesongview/<int:id>', removesong_view, name='remove-song-view'),
    path('togglefavoritesongview/', togglefavoritesong_view, name='toggle-favorite-song-view'),

    path('addchord/<int:idChord>', addchord_view, name='add-chord-view'),
    path('deletechord/', deletechord_view, name='delete-chord-view'),
]

urlpatterns += staticfiles_urlpatterns()
#For serving media:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)