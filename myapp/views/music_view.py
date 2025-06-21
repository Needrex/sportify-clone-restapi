from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, serializers
from ..serializers import music_serializers
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes
from ..models.music_model import Musician, Music, Genre, HistoryMusic
import json
from django.db.models import Prefetch
from django.http import FileResponse
import os
from ..recommendation import recommend_music

@api_view(['GET'])
def recomendations_music(request):
    user_id = request.user.id
    music = recommend_music(user_id=user_id)
    if music:
        music_data = []
        for m in music:
            music_data.append({
                'id'          : m.id,
                'name'        : m.name,
                'genres'      : [genre.genre for genre in m.genres.all()],
                'writer'      : m.writer,
                'desk'        : m.desk,
                'date_founded': m.date_founded
            }) 
            
        return Response({
            'success' : True,
            'message' : 'Successfully displayed music data',
            'data'    : music_data
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
def musician_view(request):
    try:
        recommend_music(request.user.id)
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        start = (page - 1) * page_size
        end = start + page_size
        
        musician = Musician.objects.all()[start:end]
        musician_data = []
        
        for m in musician:
            musician_data.append({
                'id'          : m.id,
                'name'        : m.name,
                'desk'        : m.desk,
                'date_founded': m.date_founded
            }) 
            
        return Response({
            'success' : True,
            'message' : 'Successfully displayed musician data',
            'data'    : musician_data
        }, status=status.HTTP_200_OK)
        
    except Musician.DoesNotExist:
        raise NotFound("Musician not found.")
    
@api_view(['GET'])
def music_view(request, id_musician):
    try:        
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        start = (page - 1) * page_size
        end = start + page_size

        music = Music.objects.prefetch_related(
            Prefetch('genres')
        )
        
        if id_musician:
            music = music.filter(musician__id=id_musician)
        elif page and page_size:
            music = music[start:end]

        music_data = []
        for m in music:
            music_data.append({
                'id'          : m.id,
                'name'        : m.name,
                'genres'      : [genre.genre for genre in m.genres.all()],
                'writer'      : m.writer,
                'desk'        : m.desk,
                'date_founded': m.date_founded
            }) 
            
        return Response({
            'success' : True,
            'message' : 'Successfully displayed music data',
            'data'    : music_data
        }, status=status.HTTP_200_OK)
        
    except Musician.DoesNotExist:
        raise NotFound("Music not found.")
    
@api_view(['GET'])
def genre_view(request):
    try:
        genre = Genre.objects.all()
        genre_data = []
        for g in genre:
            genre_data.append({
                'id'   : g.id,
                'genre': g.genre,
                'desk' : g.desk
            }) 
            
        return Response({
            'success' : True,
            'message' : 'Successfully displayed genre data',
            'data'    : genre_data
        }, status=status.HTTP_200_OK)
        
    except Genre.DoesNotExist:
        raise NotFound("Genre not found.")

@api_view(['POST'])
def musician_add(request):
    try:
        serializer = music_serializers.MusicianSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            musician = serializer.save()
            return Response({
                'success' : True,
                'message' : 'Add musician succes!',
                'data' : {
                    'id'           : musician.id,
                    'name'         : musician.name,
                    'desk'         : musician.desk,
                    'date_founded' : musician.date_founded
                }
            }, status=status.HTTP_201_CREATED)
    except serializers.ValidationError as e:
        raise ValidationError(e.detail)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def music_add(request):
    try:
        data = request.data.copy()
        genres_list = json.loads(data.get('genres', '[]'))
        data.setlist('genres', genres_list)
            
        serializer = music_serializers.MusicSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            music = serializer.save()
            return Response({
                'success' : True,
                'message' : 'Add music succes!',
                'data' : {
                    'musician_id' : music.musician.id,
                    'name'        : music.name,
                    'writer'      : music.writer,
                    'desk'        : music.desk,
                    'file'        : music.file.url,
                    'date_founded': music.date_founded
                }
            }, status=status.HTTP_201_CREATED)
    except serializers.ValidationError as e:
        raise ValidationError(e.detail)
    
@api_view(['POST'])
def genre_add(request):
    try:
        serializer = music_serializers.GenreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            genre = serializer.save()
            return Response({
                'success' : True,
                'message' : 'Add genre succes!',
                'data' : {
                    'genre'        : genre.genre,
                    'desk'         : genre.desk
                }
            }, status=status.HTTP_201_CREATED)
    except serializers.ValidationError as e:
        raise ValidationError(e.detail)

@api_view(['PUT'])
def musician_update(request, id_musician):
    try:
        musician = Musician.objects.get(id=id_musician)
        serializer = music_serializers.MusicianSerializer(musician, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            musician_updated = serializer.save()
            return Response({
                'success' : True,
                'message' : 'Update musician succes!',
                'data' : {
                    'name'         : musician_updated.name,
                    'desk'         : musician_updated.desk,
                    'date_founded' : musician_updated.date_founded
                }
            }, status=status.HTTP_200_OK)
    except Musician.DoesNotExist:
        raise NotFound("Musician not found.")
    except serializers.ValidationError as e:
        raise ValidationError(e.detail)

@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
def music_update(request, id_musician):
    try:
        music = Music.objects.get(musician=id_musician)
        data = request.data.copy()
        
        if 'genres' in data:
            genres_list = json.loads(data.get('genres', '[]'))
            data.setlist('genres', genres_list)
            
        serializer = music_serializers.MusicSerializer(music, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            music_updated = serializer.save()
            return Response({
                'success' : True,
                'message' : 'Update music succes!',
                'data' : {
                    'musician_id' : music_updated.musician.id,
                    'name'        : music_updated.name,
                    'genres'      : [genre.genre for genre in music_updated.genres.all()],
                    'writer'      : music_updated.writer,
                    'desk'        : music_updated.desk,
                    'file'        : music_updated.file.url,
                    'date_founded': music_updated.date_founded
                }
            }, status=status.HTTP_200_OK)
    except Music.DoesNotExist:
        raise NotFound("Music not found.")
    except serializers.ValidationError as e:
        raise ValidationError(e.detail)

@api_view(['PUT'])
def genre_update(request, id_genre):
    try:
        genre = Genre.objects.get(id=id_genre)
        serializer = music_serializers.GenreSerializer(genre, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            genre_updated = serializer.save()
            return Response({
                'success' : True,
                'message' : 'Update genre succes!',
                'data' : {
                    'genre' : genre_updated.genre,
                    'desk'  : genre_updated.desk
                }
            }, status=status.HTTP_200_OK)
    except Genre.DoesNotExist:
        raise NotFound("Genre not found.")
    except serializers.ValidationError as e:
        raise ValidationError(e.detail)
    
@api_view(['GET'])
def music_get(request, id_music):
    try:
        music = Music.objects.get(id=id_music)
        file_path = music.file.path
        
        if not os.path.exists(file_path):
            raise NotFound("Music file not found.")
        
        HistoryMusic.objects.create(
            user=request.user,
            music=music
        )
        
    except Music.DoesNotExist:
        raise NotFound("Music not found.")
    
    return FileResponse(open(file_path, 'rb'), content_type='audio/mpeg', as_attachment=False)