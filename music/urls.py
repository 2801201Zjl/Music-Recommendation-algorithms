from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.index, name='index'),
    path('recommendations/', views.get_recommendations_view, name='recommendations'),
    path('api/music/', views.get_music_api, name='music_api'),
    path('api/songs/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('api/songs/<int:song_id>/play/', views.record_play, name='record_play'),
] 