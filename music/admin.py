from django.contrib import admin
from .models import Song, UserBehavior, SongSimilarity

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'created_at')
    search_fields = ('title', 'artist')

@admin.register(UserBehavior)
class UserBehaviorAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'favorited', 'play_count', 'created_at')
    list_filter = ('user', 'favorited')

@admin.register(SongSimilarity)
class SongSimilarityAdmin(admin.ModelAdmin):
    list_display = ('song1', 'song2', 'similarity_score', 'created_at') 