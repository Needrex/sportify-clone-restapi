from django.urls import path
from .views import auth_view, music_view
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views.favoritmusic_view import FavoriteMusicViewSet

router = DefaultRouter()
router.register(r'favorit-music', FavoriteMusicViewSet, basename='favorite-music')

urlpatterns = [
    # Authentication
    path('register/', auth_view.regis, name='regis'),
    path('login/', auth_view.login, name='login'),
    path('logout/', auth_view.logout, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Music
    path('musician/view/', music_view.musician_view, name='musician_view'),
    path('music/view/<str:id_musician>/', music_view.music_view, name='music_view'),
    path('genre/view/', music_view.genre_view, name='genre_view'),
    
    path('musician/add/', music_view.musician_add, name='musician_add'),
    path('music/add/', music_view.music_add, name='music_add'),
    path('genre/add/', music_view.genre_add, name='genre_add'),
    
    path('musician/update/<str:id_musician>/', music_view.musician_update, name='musician_update'),
    path('music/update/<str:id_musician>/', music_view.music_update, name='music_update'),
    path('genre/update/<str:id_genre>/', music_view.genre_update, name='genre_update'),
    
    path("music/play/<str:id_music>/", music_view.music_get, name="music_get"),
    path("music/recomendations/", music_view.recomendations_music, name="music_recomendations")
]

urlpatterns += router.urls