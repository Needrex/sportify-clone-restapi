# Generated by Django 5.2.3 on 2025-06-17 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_genre_music_genre_genremusic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='music',
            name='genre',
        ),
    ]
