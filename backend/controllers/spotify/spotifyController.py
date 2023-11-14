from .spotifyKeyInfo import API_INFORMATION, AUTH_URL, TOKEN_URL, API_BASE_URL
import urllib.parse
from flask import request, jsonify
import requests

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


def getToken():
    if 'error' in request.args:
        return jsonify({"error": requests.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': API_INFORMATION[2],
            'client_id': API_INFORMATION[0],
            'client_secret': API_INFORMATION[1]
        }
        
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()
        return token_info