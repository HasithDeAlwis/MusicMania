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
    INSERT INTO top_songs (artists, song_names, valence, dancebility, release_date, top_songs_token) VALUES (%s, %s, %s, %s, %s, %s)
    """
)

UPDATE_TOP_SONGS_TABLE = (
    """UPDATE top_songs
        SET
        artists = ARRAY%s,
        song_names = ARRAY%s, 
        valence = %s, 
        dancebility = %s, 
        release_date = %s
        WHERE top_songs_token = %s;"""
)

INSERT_TOP_ARTIST = (
    """INSERT INTO top_artists (artist_name, popularity, image, genres, artist_token) VALUES(%s, %s, %s, %s, %s);"""
)

UPDATE_TOP_ARTIST = (
    """UPDATE top_songs
        SET
        artist_name = ARRAY%s,
        popularity = %s, 
        image = ARRAY%s, 
        genres = ARRAY%s, 
        WHERE artist_token = %s;"""
)

INSERT_RECENT_SONGS = (
    """INSERT INTO recent_songs (recent_songs, populairty, image, recent_songs_token) VALUES (%s, %s, %s, %s)"""
)

UPDATE_RECENT_SONGS = (
    """UPDATE recent_songs
    SET 
    recent_songs = ARRAY%s,
    popularity = %s,
    image = ARRAY%s,
    WHERE recent_songs_token = %s;"""
)

INSERT_PLAYLIST = (
    """INSERT INTO playlists (playlist_names, playlist_dancebility, playlist_valence, playlist_links, playlist_song_names, playlist_artist_names, playlist_token)
    VALUE (%s, %s, %s, %s, %s, %s, %s)"""
)

UPDATE_PLAYLIST = (
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

