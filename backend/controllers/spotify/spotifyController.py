from .spotifyKeyInfo import API_INFORMATION, AUTH_URL, TOKEN_URL, API_BASE_URL
import urllib.parse
from flask import request, jsonify, redirect, session, url_for
import requests
from datetime import datetime

#returns the url that will be called to start the OAuth Code Flow
def getSpotifyAuthURL() -> str:
    #scope of this request according to spotify API
    scope = "user-read-private user-read-email"
    
    #adding necessary params
    params = {
        'client_id': API_INFORMATION[0],
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': API_INFORMATION[2],
        'show_dialog': True
    }
    
    #creating the auth url with params
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    #returning the auth_url
    return auth_url

#get the token from the spotify API
def getToken():
    #error occured
    if 'error' in request.args:
        return jsonify({"error": requests.args['error']})
    
    #create the request body for the post request to get the token
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': API_INFORMATION[2],
            'client_id': API_INFORMATION[0],
            'client_secret': API_INFORMATION[1]
        }
        
        #post request to Spotify API to get token
        response = requests.post(TOKEN_URL, data=req_body)
        #save the token_info to json()
        token_info = response.json()
        #return it
        return token_info

#when the token expires refresh the token
def refreshToken() -> jsonify:
    #if the token is not in session then get the user to authenticate it
    if 'refresh_token' not in session: 
        return redirect('/api/spotify/authenticate')
    #check to see if the token is acc expired
    if (datetime.now().timeStamp > session['expires_at']):
        #create new body to refresh the token
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': API_INFORMATION[0],
            'client_secret': API_INFORMATION[1]
        }

    #get the toekn info
    response = requests.get(TOKEN_URL, data=req_body)
    #use json to convert token data
    new_token_info = response.json()
    return new_token_info


def getPlaylists():
    if 'access_token' not in session:
        return redirect('/login')
    
    if session['expires_at'] < datetime.now().timestamp():
        return redirect('/refresh-token')
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }
    
    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    
    playlist = response.json()
    return jsonify(playlist)