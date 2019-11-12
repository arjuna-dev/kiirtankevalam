from django.contrib import admin

# Register your models here.
from .models import Profile, Song, Chord, IsFavourite, ChordIndex, AlternateChordImage, Comment, ImmageAsComment

admin.site.register(Profile)
admin.site.register(Song)
admin.site.register(Chord)
admin.site.register(IsFavourite)
admin.site.register(ChordIndex)
admin.site.register(AlternateChordImage)
admin.site.register(Comment)
admin.site.register(ImmageAsComment)