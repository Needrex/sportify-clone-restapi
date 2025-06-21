from .models.music_model import HistoryMusic, Music

def recommend_music(user_id, limit=10):
    history_music = HistoryMusic.objects.filter(user_id=user_id).select_related('music').prefetch_related('music__genres')
    
    count_genres = {}
    excluded_ids_music = set()
    for history in history_music:
        excluded_ids_music.add(history.music.id)
        for genre in history.music.genres.all():
            if genre.id in count_genres:
                count_genres[genre.id] += 1
            else:
                count_genres[genre.id] = 1
    
    # Urutkan genre berdasarkan jumlah kemunculan
    sorted_genre_ids = [genre_id for genre_id, _ in sorted(count_genres.items(), key=lambda item: item[1], reverse=True)]
    
    # Rekomendasikan music berdasarkan genre yang sering didengar, exclude yang sudah pernah didengar
    recommend_music = Music.objects.filter(genres__in=sorted_genre_ids).exclude(id__in=excluded_ids_music).distinct()[:limit]
    
    return recommend_music