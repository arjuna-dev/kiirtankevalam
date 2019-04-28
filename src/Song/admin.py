from django.contrib import admin

# Register your models here.
from .models import User
from .models import Song
from .models import Chord

admin.site.register(User)
admin.site.register(Song)
admin.site.register(Chord)