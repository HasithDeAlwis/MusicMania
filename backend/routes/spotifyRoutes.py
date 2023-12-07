#this file will contain all the API routes that will make calls to the spotify API
from flask import Blueprint, redirect, session, request, jsonify, Response, url_for, make_response
from ..controllers.spotify.spotifyController import getSpotifyAuthURL, getToken, refreshToken, getPlaylists, getTopSongs, getRecentlyPlayed, getTopArtist, getPlaylistSongInfo, getUserProfile, addToDB, addPlaylist
from datetime import datetime
import requests 

#create blueprint for all spotify routes
spotify = Blueprint('spotify', __name__)

#authenticate will be used to intially make the call to the spotify API to start OAtuh2.0 code flow
@spotify.route('/authenticate')
def authenticate():
    #get the authorization url that spoitfy needs 
    auth_url = getSpotifyAuthURL()
    print(auth_url)
    #go to the auth_url which calls our callback route
    return make_response(jsonify({'url': auth_url}), 200)

#call back uri for the spotify API to call to atuhetnicate the API key
@spotify.route("/callback")
def setTokenInfo():
    #get the token
    getToken()
    return redirect("http://127.0.0.1:3000/profile")


#route to refresh token once it has expired
@spotify.route('/refresh-token')
def refresh_token():
    #get the new token 
    new_token_info = refreshToken()
    #change the session info
    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
    
   
@spotify.route('/get-profile', methods=["POST", "GET"]) 
def get_user_profile():
    return getUserProfile()
    
@spotify.route('/top-songs', methods=["POST"])
def get_top_songs():
    songsJSON = getTopSongs()
    return songsJSON

@spotify.route('/recently-played', methods=["POST"])
def get_recently_played():
    recentlyPlayedJSON = getRecentlyPlayed()
    return recentlyPlayedJSON

@spotify.route('/top-artists', methods=["POST"])
def get_top_artist():
    artistJSON, allGenres = getTopArtist()
    return make_response(jsonify({'artist': artistJSON, 'top-genres': allGenres}), 200)

@spotify.route('/playlist', methods=["POST"])
def get_playlist():
    playlistJSON = getPlaylists()
    return playlistJSON

@spotify.route('/get-playlist-info/<id>', methods = ["POST"])
def get_playlist_info(id):
    return getPlaylistSongInfo(id)

@spotify.route('/add-playlist/<id>', methods = ["PUT"])
def add_playlist(id):
    return addPlaylist(id)



@spotify.route('/update-user-info', methods = ["POST"])
def get_test():
    if request.method == "POST":
        #get the data from the request
        spotifyData = request.get_json()
        songs = spotifyData['top-songs']
        artists = spotifyData['top-artists']
        profile = spotifyData['user-profile']
        stats = spotifyData['user-stats']
        recent = spotifyData['recent-songs']
        playlist = spotifyData['user-playlist']
        return addToDB(songs, artists, recent, profile, stats, playlist)
        