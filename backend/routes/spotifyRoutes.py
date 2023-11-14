#this file will contain all the API routes that will make calls to the spotify API
from flask import Blueprint, redirect, session, request, jsonify
from ..controllers.spotify.spotifyController import getSpotifyAuthURL, getToken
from datetime import datetime
import requests 

#create blueprint for all spotify routes
spotify = Blueprint('spotify', __name__)

#authenticate will be used to intially make the call to the spotify API to start OAtuh2.0 code flow
@spotify.route('/authenticate')
def authenticate():
    auth_url = getSpotifyAuthURL()
    return redirect(auth_url)

@spotify.route("/callback")
def setTokenInfo():
    #get the token
    token_info = getToken()
    
    #set the session info
    session['access_token'] = token_info['access_token'] 
    session['refresh_token'] = token_info['refresh_token']
    session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']