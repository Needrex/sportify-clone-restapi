from rest_framework.viewsets import ModelViewSet
from ..models.music_model import FavoriteMusic
from ..serializers.favoritmusic_serializer import FavoriteMusicSerializer
from rest_framework import status
from rest_framework.response import Response


class FavoriteMusicViewSet(ModelViewSet):
    queryset = FavoriteMusic.objects.all()
    serializer_class = FavoriteMusicSerializer
    
    def get_queryset(self):
        user = self.request.user
        return FavoriteMusic.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success' : True,
            'message' : 'Successfully displayed favorit music data',
            'data'    : serializer.data
        }, status=status.HTTP_200_OK)

