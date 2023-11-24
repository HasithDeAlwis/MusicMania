from .spotifyKeyInfo import API_INFORMATION, AUTH_URL, TOKEN_URL, API_BASE_URL
import urllib.parse
from flask import request, jsonify, redirect, session, url_for, abort, Response
import requests
from datetime import datetime
from ...database import connection, INSERT_RECENT_SONGS, INSERT_TOP_SONGS, CHECK_IF_ALREADY_ADDED, UPDATE_RECENT_SONGS, UPDATE_TOP_SONGS, INSERT_TOP_ARTISTS, UPDATE_TOP_ARTISTS, UPDATE_PLAYLISTS, INSERT_PLAYLISTS

#returns the url that will be called to start the OAuth Code Flow
def getSpotifyAuthURL() -> str:
    #scope of this request according to spotify API
    scope = "user-read-private user-read-email playlist-read-private user-top-read user-read-recently-played"
    
    print("Hope this works", API_INFORMATION[0])
    
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
    #print auth url
    print(auth_url)
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
    try:    
        #make url for songs
        songURL = API_BASE_URL + '/me/top/tracks?limit=50'
        topSongsInfo = [] #stores top songs info
        currentArtistArray = [] #stores artist for a given song
    
  
        #make the request
        results = requests.get(songURL, headers=headers)
        #make results to dict
        results = results.json()
        #get only the itmes
        topSongsResult = results["items"]
        #enumerate through itmes
        for song in topSongsResult:
            if song:
                #get the artists
                for artist in song['artists']:
                    #add the artist to the array
                    currentArtistArray.append(artist['name'])
                
                id = song['id']
                name = song['name']
                popularity = float(song['popularity']) #how popular the song is on a scale of 0-100
                cover_image =  song['album']['images'][0]['url']
                release_date = song['album']['release_date']
                release_date = str(release_date)
                artists = currentArtistArray
                song_link =  song['external_urls']['spotify']
                #make the array empty for the next song 
                currentArtistArray = []
                with connection:
                    with connection.cursor() as cursor:
                        #check to see if the user already has song info added to their account
                        #cursor.execute(CHECK_IF_ALREADY_ADDED, ('top_songs', 'top_songs_token', session['userInfo'],))
                        exists = None
                        if exists:
                            #yes it exists, so just update
                            cursor.execute(UPDATE_TOP_SONGS, (id, name, artists, song_link, popularity, release_date, cover_image,))
                        else:
                            #no it doesnt exists, so create a new rows for 
                            cursor.execute(INSERT_TOP_SONGS, (id, name, artists, song_link, popularity, release_date, cover_image,))
        return Response("Added top songs to database successfully!", status=201)
    except Exception:
        return Response("Server ERROR", status=404)


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
        for item in recentlyPlayedResults:
            song = item["track"]
            if song:
                #get the artists
                for artist in song['artists']:
                    #add the artist to the array
                    currentArtistArray.append(artist['name'])
                
                #collect needed info respective variables
                id = song['id'],
                song_name =  song['name'],
                popularity = song['popularity'], #how popular the song is on a scale of 0-100
                cover_images = song['album']['images'][0]['url'],
                artists = currentArtistArray,
                song_link =  song['external_urls']['spotify']

                #open connection to the database
                with connection:
                    with connection.cursor() as cursor:
                        #check to see if the users info has already been added to the db
                        #cursor.execute(CHECK_IF_ALREADY_ADDED, ('top_songs', 'top_songs_token', session['userInfo'],))
                        exists = None
                        if exists:
                            #it has been added already so just update their recent songs
                            cursor.execute(UPDATE_RECENT_SONGS, (id, song_name, artists, song_link, [cover_images], popularity,))
                        else:
                            #it hasnt been added to now create new rows with their recent songs
                            cursor.execute(INSERT_RECENT_SONGS, (id, song_name, artists, song_link, [cover_images], popularity,))
                    #make the array empty for the next song 
                    currentArtistArray = []
        return Response("Successfully added recent songs to database!", status=201)
    except Exception:
        return Response("Server ERROR", status=404)
        

    
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
    try:
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
                #add the top artist info to their respective variables
                name = artist['name'],
                artists_id = artist['id']
                genres = artist['genres'],
                images = artist['images'][0]['url'],
                popularity =  artist['popularity']
                artists_link = artist['external_urls']['spotify']
                
                #open connection to database
                with connection:
                    with connection.cursor() as cursor:
                        #check if any info has already been added for the associated user
                        #cursor.execute(CHECK_IF_ALREADY_ADDED, ('top_songs', 'top_songs_token', session['userInfo'],))
                        exists = None
                        if exists:
                            #the users artists are already in the db, so just update it
                            cursor.execute(UPDATE_TOP_ARTISTS, (artists_id, name, genres, images, artists_link, popularity,))                    
                        else:
                            #the users artists are not in the db, so add it
                            cursor.execute(INSERT_TOP_ARTISTS, (artists_id, name, genres, images, artists_link, popularity,))
        #give back the array of dict with info
        return Response("Successfully Added Artists Info to DB", status=201)
    
    except Exception:
        return Response("Server ERROR", status=201)



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
                    # print(songFeatures)
                    
                    #add the important info their respective variables
                    id = item['id']
                    name = item['name'],
                    link = item['external_urls']['spotify'],
                    images = item['images'][0]['url'],
                    spotifyLink = item['tracks']['href']
                    
                    #open connection to database
                    with connection:
                        with connection.cursor() as cursor:
                            #cursor.execute(CHECK_IF_ALREADY_ADDED, ('top_songs', 'top_songs_token', session['userInfo'],))
                            exists = None
                            #if there is nothing to a db associated with the user then make these calls 
                            if exists:
                                #update the playlists info with new data
                                cursor.execute(UPDATE_PLAYLISTS, (id, name, link, images, spotifyLink))                    
                            else:
                                #insert new data into the db for a new user
                                cursor.execute(INSERT_PLAYLISTS, (id, name, link, images, spotifyLink))
                    
                    
            #if there is a next then we can get the next value
            if (results['next']):
                #set the playlistURL to the next playlist
                playlistURL  = results['next']
            else:
                #leave the loop
                break
            
        #return the dict
        return Response("Successfully Added Playlist Info to DB", status=201)
    #error with server
    except Exception:
        abort(Response(Exception, status=401))

#get the info of a specific songs on a spotify playlist        
def getPlaylistSongInfo(playlistID: str) -> list:
    #create the endpoint for the track details for a playlist
    songsAPIEndpoint = API_BASE_URL + '/playlists/' + playlistID + '/tracks'
    
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
    try:
        #get the results
        results = requests.get(songsAPIEndpoint, headers=headers)
        results = results.json()
        
        #we only want the items object
        tracksInfo = results['items']
        
        #arrays that will hold all the info
        allArtists = []
        allSongs = []
        
        #store the songIds in a string for the track analysis
        songIds = ""
        
        #save the artists for a song in a single string (this is because of SQL not allowing multi-deminsonal arrays of different sizes)
        artistsForSong = ""
        
        #count is 0
        count = 0
        
        #loop through every track
        for item in tracksInfo:
            #take the song title
            allSongs.append(item['track']['name'])
            #take the name of the artist
            artists =  item['track']['album']['artists']
            
            #loop through the artist
            for index, artist in enumerate(artists):
                #check to see if the index is 0 so we won't add an @
                if (index == 0):
                    artistsForSong = artist['name']
                else:
                    #add the artist list
                    artistsForSong += "@" + artist['name'] #the @ is for future logic when distingushing between different arists
            
            #add this to the artists to the array 
            allArtists.append(artistsForSong)
            
            #make this empty again for the next song
            artistsForSong = ""
            
            #for the first 100 songs of the playlist check add their song id
            if count < 100:
                if count != 0:
                    #get the ID
                    songIds += ',' + item['track']['id']
                else:
                    songIds = item['track']['id']
                count += 1
        #get the track features of a song
        trackFeatures = analyzeSongs(songIds)
        
        #put all the song info into a dict 
        allSongsInfo = {
            "artists": allArtists, 
            "titles": allSongs, 
            "valence": trackFeatures[0],
            "danceability": trackFeatures[1]
        }
        
        #return the dictionary 
        return allSongsInfo
    except:
        return Response("API ERROR", status=401)

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
    
    #set valence and avg to 0 for counting 
    valenceAvg = 0
    dancebilityAvg = 0
    
    #create url to analyze all the tracks
    songAnalysisEndpoint = API_BASE_URL + '/audio-features?ids=' + songIds
    
    try:
        #get all the songs
        songAnalysingResults = requests.get(songAnalysisEndpoint, headers=headers)
        songAnalysingResults = songAnalysingResults.json()
        
        #only want audio_features object
        songAnalysingResults = songAnalysingResults['audio_features']
        #loop through every song
        for song in songAnalysingResults:
            #increment dancebility and valence
            dancebilityAvg += song['danceability']
            valenceAvg += song['valence'] 
            
        #make songIds into an array then get its length to find num of songs
        numberOfSongs = len(songIds.split(','))
        
        #calc valence and dancebility of playlist
        valenceAvg = valenceAvg / numberOfSongs
        dancebilityAvg = dancebilityAvg / numberOfSongs

        #add this to an array 
        songFeaturesInfo = [valenceAvg, dancebilityAvg]
        #return the info
        return songFeaturesInfo
    
    except Exception: 
        return Response("API ERROR", status=401)
        
        
    