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

from Song.views import record_view, song_view, profile_view, main_view, kiirtanfav_view, kiirtanall_view, kiirtanuploads_view, kiirtanfeed_view, psfav_view, psall_view, psuploads_view, psfeed_view, bhajanfav_view, bhajanall_view, bhajanuploads_view, bhajanfeed_view, signup, user_login, addsong_view, deletesong_view, addchord_view, deletechord_view, createsong_view, editchords_view



urlpatterns = [
    path('', main_view),
    path('kiirtanfav/', kiirtanfav_view),
    path('kiirtanfeed/', kiirtanfeed_view),
    path('kiirtanall/', kiirtanall_view),
    path('kiirtanuploads/', kiirtanuploads_view),
    path('psfav/', psfav_view),
    path('psfeed/', psfeed_view),
    path('psall/', psall_view),
    path('psuploads/', psuploads_view),
    path('bhajanfav/', bhajanfav_view),
    path('bhajanfeed/', bhajanfeed_view),
    path('bhajanall/', bhajanall_view),
    path('bhajanuploads/', bhajanuploads_view),
    path('song/', song_view),
    path('record/', record_view),
    path('createsong/', createsong_view, name='create-song-view'),
    path('editchords/', editchords_view),
    path('profile/', profile_view),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='user_login'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('addsongview/<int:id>', addsong_view, name='add-song-view'),
    path('deletesongview/<int:id>', deletesong_view, name='delete-song-view'),

    path('addchord/<int:idChord>', addchord_view, name='add-chord-view'),
    path('deletechord/', deletechord_view, name='delete-chord-view'),
]

urlpatterns += staticfiles_urlpatterns()