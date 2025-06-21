from rest_framework import serializers
from ..models.music_model import Musician, Music, Genre

class MusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Musician
        fields  = ['name','desk','date_founded']
        
    def validate_name(self, value):
        MIN_LENGTH = 3  
        if len(value) < MIN_LENGTH:
            raise serializers.ValidationError(f"Name is too short! ( {MIN_LENGTH} )")
        
        return value
    
    def validate_desk(self, value):
        MIN_LENGTH = 10  
        if len(value) < MIN_LENGTH:
            raise serializers.ValidationError(f"Desk is too short! ( {MIN_LENGTH} )")
        
        return value
    
class MusicSerializer(serializers.ModelSerializer):
    musician = serializers.PrimaryKeyRelatedField(
        queryset=Musician.objects.all(),
        write_only=True
    )
    
    genres = serializers.PrimaryKeyRelatedField(
    queryset=Genre.objects.all(),
    many=True  
    )
        
    class Meta:
        model   = Music
        fields  = ['musician','name','genres','writer','desk','file','date_founded']
        
    def validate_name(self, value):
        MIN_LENGTH = 3  
        if len(value) < MIN_LENGTH:
            raise serializers.ValidationError(f"Name is too short! ( {MIN_LENGTH} )")
        return value
    
    def validate_genres(self, value):       
        if len(value) > 3:
            raise serializers.ValidationError("Maksimal 3 genre saja.")

        if len(value) != len(set(value)):
            raise serializers.ValidationError("Genre tidak boleh duplikat.")
        
        return value

    def validate_writer(self, value):
        MIN_LENGTH = 3  
        if len(value) < MIN_LENGTH:
            raise serializers.ValidationError(f"Writer is too short! ( {MIN_LENGTH} )")
        return value

    def validate_desk(self, value):
        MIN_LENGTH = 10  
        if len(value) < MIN_LENGTH:
            raise serializers.ValidationError(f"Desk is too short! ( {MIN_LENGTH} )")
        return value

    def validate_file(self, value):
        max_size = 5 * 1024 * 1024  
        allowed_extensions = ['mp3', 'wav', 'ogg']

        if value.size > max_size:
            raise serializers.ValidationError("File size must be under 5MB.")

        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError("Unsupported file extension.")

        return value
    
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Genre
        fields  = ['genre','desk']
        
    def validate_genre(self, value):
        MIN_LENGTH = 3  
        if len(value) < MIN_LENGTH:
            raise serializers.ValidationError(f"Genre is too short! ( {MIN_LENGTH} )")
        return value
    
    def validate_desk(self, value):
        MIN_LENGTH = 10  
        if len(value) < MIN_LENGTH:
            raise serializers.ValidationError(f"Desk is too short! ( {MIN_LENGTH} )")
        return value




