from rest_framework import serializers
from ..models.music_model import FavoriteMusic

class FavoriteMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMusic
        fields = ['user', 'music']
    
    def validate(self, attrs):
        user = attrs.get('user')
        music = attrs.get('music')

        if FavoriteMusic.objects.filter(user=user, music=music).exists():
            raise serializers.ValidationError("This music is already in your favorites.")

        return attrs