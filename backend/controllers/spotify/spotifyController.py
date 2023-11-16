from .spotifyKeyInfo import API_INFORMATION, AUTH_URL, TOKEN_URL, API_BASE_URL
import urllib.parse
from flask import request, jsonify, redirect, session, url_for, abort, Response
import requests
from datetime import datetime

#returns the url that will be called to start the OAuth Code Flow
def getSpotifyAuthURL() -> str:
    #scope of this request according to spotify API
    scope = "user-read-private user-read-email playlist-read-private user-top-read user-read-recently-played"
    
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

#a function to get the top songs
def getTopSongs() -> dict:
    #basic authentication
    if 'access_token' not in session:
        return redirect('/login')
    
    #check refresh token
    if session['expires_at'] < datetime.now().timestamp():
        return redirect('/refresh-token')
    
    #check header
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }
    
    #make url for songs
    songURL = API_BASE_URL + '/me/top/tracks?limit=50'
    topSongsInfo = [] #stores top songs info
    currentArtistArray = [] #stores artist for a given song
    
    try:
        #make the request
        results = requests.get(songURL, headers=headers)
        #make results to dict
        results = results.json()
        
        #get only the itmes
        topSongsResult = results["items"]
        #enumerate through itmes
        for index, song in enumerate(topSongsResult):
            if song:
                #add needed info
                topSongsInfo.append({
                        "id": song['id'],
                        "name": song['name'],
                        "popularity": song['popularity'], #how popular the song is on a scale of 0-100
                        "image": song['album']['images']
                    }) 
                #get the artists
                for artist in song['artists']:
                    #add the artist to the array
                    currentArtistArray.append(artist['name'])
                    
                #add that artist to the array 
                topSongsInfo[index]['artists'] = currentArtistArray  
                #make the array empty for the next song 
                currentArtistArray = []
        return topSongsInfo

    except Exception:
        abort(Response("Spotify API Error", status=401))


def getRecentlyPlayed():
    #basic authentication
    if 'access_token' not in session:
        return redirect('/login')
    
    #check refresh token
    if session['expires_at'] < datetime.now().timestamp():
        return redirect('/refresh-token')
    
    #check header
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }
    
    recentlyPlayedURL = API_BASE_URL + '/me/player/recently-played?limit=50'
    
    try:
        #get the results of the recently played
        results = requests.get(recentlyPlayedURL, headers=headers)
        #make it a dict
        results = results.json()
        
        #where we store the recent songs
        recentSongInfo = []
        currentArtistArray = [] #store the artists for each song
        
        #get only the itmes
        recentlyPlayedResults = results["items"]
        #enumerate through itmes
        for index, item in enumerate(recentlyPlayedResults):
            song = item["track"]
            if song:
                #add needed info
                recentSongInfo.append({
                    "id": song['id'],
                    "name": song['name'],
                    "popularity": song['popularity'], #how popular the song is on a scale of 0-100
                    "images": song['album']['images']
                    }) 
                #get the artists
                for artist in song['artists']:
                    #add the artist to the array
                    currentArtistArray.append(artist['name'])
                        
                #add that artist to the array 
                recentSongInfo[index]['artists'] = currentArtistArray  
                #make the array empty for the next song 
                currentArtistArray = []
        return recentSongInfo
    except:
        abort(Response("Error with Spotify API", status=400))
    
#get the top artists    
def getTopArtist():
    #basic authentication
    if 'access_token' not in session:
        return redirect('/api/spotify/authenticate')
    
    #check refresh token
    if session['expires_at'] < datetime.now().timestamp():
        return redirect('/api/spotify/refresh-token')
    
    #check header
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }
    #create url for the top artists
    topArtistsURL = API_BASE_URL + '/me/top/artists?limit=50'
    #get request for artists data
    results = requests.get(topArtistsURL, headers=headers)
    #convert to dict
    results = results.json()
    #get only the top artists
    topArtists = results["items"]
    #set the artists array to be -
    topArtistInfo = []
    for artist in topArtists:
        if artist:
            #the top artist info
            topArtistInfo.append(
                {
                    #get their name, genre, popularity and images associated with the artists
                    "name": artist['name'],
                    "genres": artist['genres'],
                    "images": artist['images'],
                    "popularity": artist['popularity']
                }
            )
    #give back the array of dict with info
    return topArtistInfo



#Get a users total playlist then remove the playlist that the users don't listen to much
def getPlaylists():
    #basic authentication
    if 'access_token' not in session:
        return redirect('/login')
    
    #check if token expired
    if session['expires_at'] < datetime.now().timestamp():
        return redirect('/refresh-token')
    #check header
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }
    
    #only take certain info from the playlists returned
    playlistInfo = []
    #playlistURL
    playlistURL = API_BASE_URL + '/me/playlists?limit=50&offset=0'
    #get all the playlist from a user
    try:
        while True:
            #get a page of results
            results = requests.get(playlistURL, headers=headers)
            #turn to dict to make it subscriptable
            results = results.json()
            #get only the items
            playlistPage = results["items"]
            
            
            
            #get the playlist
            for item in playlistPage:
                if (item):
                    songLink =  item['tracks']['href']
                    songFeatures = getPlaylistSongInfo(songLink)
                    # print(songFeatures)
                    #add the important info the dict
                    playlistInfo.append({
                        "id": item['id'],
                        "name": item['name'],
                        "link": item['external_urls']['spotify'],
                        "images": item['images'],
                    })
                return playlistInfo
            
            #if there is a next then we can get the next value
            if (results['next']):
                #set the playlistURL to the next playlist
                playlistURL  = results['next']
            else:
                #leave the loop
                break
        #return the dict
        return playlistInfo
    #error with server
    except Exception:
        abort(Response(Exception, status=401))
        
def getPlaylistSongInfo(songsAPIEndpoint: str) -> tuple:
    #basic authentication
    if 'access_token' not in session:
        return redirect('/login')
    
    #check if token expired
    if session['expires_at'] < datetime.now().timestamp():
        return redirect('/refresh-token')
    #check header
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }
    
    results = requests.get(songsAPIEndpoint, headers=headers)
    results = results.json()

    tracksInfo = results['items']
    allArtists = []
    allSongs = []
    songIds = ""
    
    artistsForSong = ""
    
    count = 0
    
    for item in tracksInfo:
        allSongs.append(item['track']['name'])
        artists =  item['track']['album']['artists']
        
        for index, artist in enumerate(artists):
            if (index == 0):
                artistsForSong = artist['name']
            else:
                    
                artistsForSong += "@" + artist['name'] 
                
        allArtists.append(artistsForSong)
        
        artistsForSong = ""
        
        if count < 100:
            if count != 0:
                songIds += ',' + item['track']['id']
            else:
                songIds = item['track']['id']
            count += 1
    
    trackFeatures = analyzeSongs(songIds)
    allSongsInfo = [allArtists, allSongs, trackFeatures]
    #print(allSongsInfo)
    return allSongsInfo

def analyzeSongs(songIds: str):
    
    #basic authentication
    if 'access_token' not in session:
        return redirect('/login')
    
    #check if token expired
    if session['expires_at'] < datetime.now().timestamp():
        return redirect('/refresh-token')
    #check header
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }
    
    valenceAvg = 0
    dancebilityAvg = 0
    songAnalysisEndpoint = API_BASE_URL + '/audio-features?ids=' + songIds
    print(songAnalysisEndpoint)
    songAnalysingResults = requests.get(songAnalysisEndpoint, headers=headers)
    songAnalysingResults = songAnalysingResults.json()
    print(songAnalysingResults)
    songAnalysingResults = songAnalysingResults['audio_features']
    for song in songAnalysingResults:
        dancebilityAvg += song['danceability']
        valenceAvg += song['valence'] 
    
    valenceAvg = valenceAvg / len(songIds)
    dancebilityAvg = dancebilityAvg / len(songIds)
    songFeaturesInfo = [valenceAvg, dancebilityAvg]
    return songFeaturesInfo
        
        
    