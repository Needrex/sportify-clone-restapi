from django.db import models
from ..utils import custom_upload_to
import uuid
from django.contrib.auth.models import User

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

class HistoryMusic(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    date_play = models.DateTimeField(auto_now=True)