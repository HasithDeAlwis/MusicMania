import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

CREATE_USER_TABLE = (
    """CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY, 
        first_name TEXT,
        last_name TEXT, 
        user_name TEXT,
        email TEXT,
        password TEXT,
        token TEXT,
        confirmed BOOLEAN DEFAULT FALSE);"""
)

INSERT_USER = (
    """INSERT INTO users (first_name, last_name, user_name, email, password, token) VALUES (%s, %s, %s, %s, %s, %s);
    """
)

INSERT_TOP_SONGS = (
    """
    INSERT INTO top_songs (song_id, song_name, artists_name, song_link, popularity, release_date, cover_images) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
)

UPDATE_TOP_SONGS = (
    """UPDATE top_songs
        SET
        song_id = %s
        song_names = %s, 
        artists_name = %s, 
        song_link = %s, 
        popularity = %s,
        release_date = %s,
        cover_images = %s
        WHERE top_songs_token = %s;"""
)

INSERT_TOP_ARTISTS = (
    """INSERT INTO top_artists (artist_id, artist_name, genres, cover_image, artist_link, popularity) VALUES(%s, %s, %s, %s, %s, %s);"""
)

UPDATE_TOP_ARTISTS = (
    """UPDATE top_songs
        SET
        artist_id = %s,
        artist_name = %s,
        popularity = %s, 
        image = ARRAY%s, 
        genres = ARRAY%s, 
        WHERE artist_token = %s;"""
)

INSERT_RECENT_SONGS = (
    """INSERT INTO recent_songs (song_id, song_name, artists_name, song_link, cover_images, popularity) VALUES (%s, %s, %s, %s, %s, %s)"""
)

UPDATE_RECENT_SONGS = (
    """UPDATE recent_songs
    SET 
    song_id = %s
    song_name = %s
    artists_name = %s,
    song_link = %s
    cover_images = %s
    popularity = %s,
    WHERE %s = %s
    """
)



CHECK_IF_ALREADY_ADDED = (
    """SELECT * FROM %s 
    WHERE %s = %s"""
)


UPDATE_RECENT_SONGS = (
    """UPDATE recent_songs
    SET 
    recent_songs = ARRAY%s,
    popularity = %s,
    image = ARRAY%s,
    WHERE recent_songs_token = %s;"""
)

INSERT_PLAYLISTS = (
    """INSERT INTO playlists (playlist_id, playlist_name, playlist_link, playlist_cover, spotify_link) VALUES (%s, %s, %s, %s, %s)"""
)

UPDATE_PLAYLISTS = (
    """UPDATE playlist
    SET
    playlist_name = ARRAY%s,
    playlist_dancebility = ARRAY%s,"""
)
FIND_TOKEN = (
    """SELECT * FROM users
    WHERE token = (%s)
    LIMIT 1"""
)

VERIFY_EMAIL = (
    """UPDATE users
    SET confirmed = TRUE
    WHERE token = (%s)"""
)


FIND_SAME_ACCOUNT = (
    """SELECT * from users
    WHERE email = %s or user_name = %s
    LIMIT 1;"""
)

