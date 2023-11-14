#this file will contain all the API routes that will make calls to the spotify API
from flask import Blueprint, redirect, session, request, jsonify, Response, url_for
from ..controllers.spotify.spotifyController import getSpotifyAuthURL, getToken, refreshToken, getPlaylists, getTopSongs, getRecentlyPlayed, getTopArtist
from datetime import datetime
import requests 

#create blueprint for all spotify routes
spotify = Blueprint('spotify', __name__)

#authenticate will be used to intially make the call to the spotify API to start OAtuh2.0 code flow
@spotify.route('/authenticate')
def authenticate():
    #get the authorization url that spoitfy needs 
    auth_url = getSpotifyAuthURL()
    #go to the auth_url which calls our callback route
    return redirect(auth_url)

#call back uri for the spotify API to call to atuhetnicate the API key
@spotify.route("/callback")
def setTokenInfo():
    #get the token
    token_info = getToken()
    
    #set the session info
    session['access_token'] = token_info['access_token'] 
    session['refresh_token'] = token_info['refresh_token']
    session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
    playlistRoute = url_for('spotify.get_playlist')
    return redirect(playlistRoute)

#route to refresh token once it has expired
@spotify.route('/refresh-token')
def refresh_token():
    #get the new token 
    new_token_info = refreshToken()
    #change the session info
    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
    
@spotify.route('/top-songs')
def get_top_songs():
    songsJSON = getTopSongs()
    return songsJSON

@spotify.route('/recently-played')
def get_recently_played():
    recentlyPlayedJSON = getRecentlyPlayed()
    return recentlyPlayedJSON


@spotify.route('/top-artists')
def get_top_artist():
    artistJSON = getTopArtist()
    return artistJSON

@spotify.route('/playlist')
def get_playlist():
    playlistJSON = getPlaylists()
    return playlistJSON