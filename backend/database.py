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
    INSERT INTO top_songs (song_id, song_name, artists_name, song_link, popularity, release_date, cover_images, top_songs_token) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
)

UPDATE_TOP_SONGS = (
    """UPDATE top_songs
    SET
    song_id = %s,
    song_name = %s,
    artists_name = %s, 
    song_link = %s,
    popularity = %s,
    release_date = %s,
    cover_images = %s
    WHERE top_songs_token = %s;
    """
)

DELTE_FROM_TABLE = (
    """DELETE FROM {} 
    WHERE {} = %s;"""
)

INSERT_TOP_ARTISTS = (
    """INSERT INTO top_artists (artist_id, artist_name, genres, cover_image, artist_link, popularity, top_artists_token) VALUES(%s, %s, %s, %s, %s, %s, %s);"""
)

INSERT_SPOTIFY_PROFILE = (
    """INSERT INTO spotify_profile (display_name, link_to_profile, spotify_id, profile_picture, valence, energy, danceability, popularity, spotify_profile_token) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
)
UPDATE_SPOTIFY_PROFILE = (
    """UPDATE spotify_profile
    SET 
    display_name = %s,
    link_to_profile = %s,
    spotify_id = %s,
    profile_picture = %s,
    valence = %s,
    energy = %s,
    danceability = %s,
    popularity = %s
    WHERE spotify_profile_token = %s;"""
)


UPDATE_TOP_ARTISTS = (
    """UPDATE top_artists
        SET
        artist_id = %s,
        artist_name = %s,
        genres = %s,
        cover_image = %s, 
        artist_link = %s,
        popularity = %s
        WHERE top_artists_token = %s;"""
)

INSERT_RECENT_SONGS = (
    """INSERT INTO recent_songs (song_id, song_name, artists_name, song_link, cover_images, recent_songs_token) VALUES (%s, %s, %s, %s, %s, %s)"""
)

UPDATE_RECENT_SONGS = (
    """UPDATE recent_songs
    SET 
    song_id = %s,
    song_name = %s,
    artists_name = %s,
    song_link = %s,
    cover_images = %s
    WHERE recent_songs_token = %s;
    """
)



CHECK_IF_ALREADY_ADDED = (
    """SELECT * FROM {}
    WHERE {} = %s"""
)


INSERT_PLAYLISTS = (
    """INSERT INTO playlists (playlist_id, playlist_name, playlist_link, playlist_cover, playlist_token) VALUES (%s, %s, %s, %s, %s)"""
)

UPDATE_PLAYLISTS = (
    """UPDATE playlists
    SET
    playlist_id = %s,
    playlist_name = %s,
    playlist_link = %s,
    playlist_cover = %s
    WHERE playlist_token = %s;
    """
)
FIND_TOKEN = (
    """SELECT * FROM users
    WHERE token = %s
    LIMIT 1"""
)

FIND_PROFILE = (
    """SELECT * FROM spotify_profile
    WHERE spotify_profile_token = %s
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

FIND_INSTANCE_OF_IN_TOP_SONGS = (
    """SELECT * FROM top_songs
    WHERE 
    UPPER(song_name) LIKE UPPER(%s)
    OR UPPER (artists_name) LIKE UPPER(%s)"""
)

FIND_INSTANCE_OF_IN_RECENT_SONGS = (
    """SELECT * FROM recent_songs
    WHERE 
    UPPER(song_name) LIKE UPPER(%s)
    OR UPPER(artists_name) LIKE UPPER(%s)"""
)

FIND_INSTANCE_OF_IN_TOP_ARTISTS= (
    """
    SELECT * FROM top_artists
    WHERE 
    UPPER(artist_name) LIKE UPPER(%s)"""
)

GET_ALL_INFO = (
    """SELECT 
    top_songs.song_name AS top_songs_name, 
    top_songs.song_link AS top_songs_link, 
    top_songs.artists_name AS top_songs_artist,
    top_songs.cover_images As top_songs_image,
    top_artists.artist_name AS top_artists_name,
    top_artists.cover_image AS top_artists_image,
    top_artists.genres AS top_artists_genres,
    top_artists.artist_link AS top_artists_link,
    recent_songs.song_name AS recent_songs_name,
    recent_songs.song_link AS recent_songs_link,
    recent_songs.artists_name AS recent_songs_artists,
    recent_songs.cover_images AS recent_songs_images,
    spotify_profile.display_name AS spotify_name,
    spotify_profile.spotify_id AS spotify_id,
    spotify_profile.profile_picture AS spotify_profile_picture,
    spotify_profile.link_to_profile AS spotify_profile_link,
    spotify_profile.valence AS spotify_valence,
    spotify_profile.danceability AS spotify_danceability,
    spotify_profile.energy AS spotify_energy,
    spotify_profile.popularity AS spotify_popularity,
    playlists.playlist_id AS playlist_id,
    playlists.playlist_name as playlist_name,
    playlists.playlist_cover as playlist_cover
FROM users
JOIN top_artists ON users.token = top_artists.top_artists_token
JOIN top_songs ON top_artists.top_artists_token = top_songs.top_songs_token
JOIN recent_songs ON top_songs.top_songs_token = recent_songs.recent_songs_token
JOIN spotify_profile ON recent_songs.recent_songs_token = spotify_profile.spotify_profile_token
JOIN playlists ON spotify_profile.spotify_profile_token = playlists.playlist_token
WHERE users.token = %s"""
)

GET_FAV_SONG_AND_ARTISTS_PREVIEW = (
    """
    SELECT 
    top_songs.song_name AS top_song_name,
    top_songs.artists_name AS top_song_artist,
    top_artists.artist_name AS top_artists_name
    FROM top_artists 
    JOIN top_songs ON top_artists.top_artists_token = top_songs.top_songs_token
    WHERE top_songs.top_songs_token = %s
    """
)

GET_USER_PFP = (
    """SELECT profile_picture
    FROM spotify_profile
    WHERE spotify_profile_token = %s
    """
)