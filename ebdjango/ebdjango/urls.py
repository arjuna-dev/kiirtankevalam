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
from django.urls import path, include
#For serving media:
from django.conf import settings
from django.conf.urls.static import static
from Song.views import mainrenderer_view, song_view, profile_view, signup, deletechord_view, createsong_view, editchords_view, addchord_view, togglefavoritesong_view, undertab_view, overtab_view,lalita_view

urlpatterns = [
    path('', mainrenderer_view),
    path('lalita/', lalita_view),
    path('overtab/', overtab_view, name='overtab-view'),
    path('undertab/', undertab_view, name='undertab-view'),
    path('song/<int:songid>', song_view, name='song-view'),
    path('createsong/', createsong_view, name='create-song-view'),
    path('editchords/', editchords_view, name='edit-chords-view'),
    path('profile/', profile_view),
    path('signup/', signup, name='signup'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('togglefavoritesongview/', togglefavoritesong_view, name='toggle-favorite-song-view'),
    path('addchord/<int:idChord>', addchord_view, name='add-chord-view'),
    path('deletechord/', deletechord_view, name='delete-chord-view'),
]

urlpatterns += staticfiles_urlpatterns()
#For serving media:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)