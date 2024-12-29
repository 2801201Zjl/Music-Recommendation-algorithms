from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    audio_url = models.URLField(default='https://example.com/default-audio.mp3')
    cover_url = models.URLField(default='https://example.com/default-cover.jpg')
    lyrics = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.artist}"

class UserBehavior(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    clicked = models.BooleanField(default=False)  # 点击行为
    favorited = models.BooleanField(default=False)  # 收藏行为
    play_count = models.IntegerField(default=0)  # 播放次数
    last_played = models.DateTimeField(auto_now=True)  # 最后播放时间
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')

class SongSimilarity(models.Model):
    song1 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='similar_to')
    song2 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='similar_from')
    similarity_score = models.FloatField()  # 相似度分数
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('song1', 'song2') 