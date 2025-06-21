from django.db import models
from ..utils import custom_upload_to
import uuid
from django.contrib.auth.models import User
import os
from django.conf import settings


class Musician(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    name = models.CharField(max_length=30)
    desk = models.CharField(max_length=250)
    date_founded = models.DateField()
    
class Genre(models.Model):
    genre = models.CharField(max_length=30)
    desk = models.CharField(max_length=250)
    
class Music(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    genres = models.ManyToManyField(Genre)
    writer = models.CharField(max_length=30)
    desk = models.CharField(max_length=250)
    file = models.FileField(upload_to=custom_upload_to)
    date_founded = models.DateField()
    
    def save(self, *args, **kwargs):
        MUSIC_PATH = os.path.join(settings.MEDIA_ROOT, 'music')
        if MUSIC_PATH and not os.path.exists(MUSIC_PATH):
            os.makedirs(MUSIC_PATH)
        super().save(*args, **kwargs)

class HistoryMusic(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    date_play = models.DateTimeField(auto_now=True)
    
class FavoriteMusic(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True)