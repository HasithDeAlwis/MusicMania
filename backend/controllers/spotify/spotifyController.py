from .spotifyKeyInfo import API_INFORMATION, AUTH_URL, TOKEN_URL, API_BASE_URL
import urllib.parse
from flask import request, jsonify, redirect, session, url_for, abort, Response, make_response
import requests
from datetime import datetime
from ...database import GET_FAV_SONG_AND_ARTISTS_PREVIEW, connection, INSERT_RECENT_SONGS, INSERT_TOP_SONGS, INSERT_TOP_ARTISTS, UPDATE_TOP_ARTISTS, UPDATE_PLAYLISTS, INSERT_PLAYLISTS, CHECK_IF_ALREADY_ADDED, UPDATE_RECENT_SONGS, UPDATE_TOP_SONGS, INSERT_SPOTIFY_PROFILE, UPDATE_SPOTIFY_PROFILE, FIND_INSTANCE_OF_IN_RECENT_SONGS, FIND_INSTANCE_OF_IN_TOP_SONGS, FIND_INSTANCE_OF_IN_TOP_ARTISTS, FIND_PROFILE, GET_ALL_INFO
import json
from psycopg2 import extras



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
        
        #set the session info
        session['access_token'] = token_info['access_token'] 
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        #tell flask we modified the session so it updates right away
        session.modified = True


#when the token expires refresh the token
def refreshToken() -> jsonify:
    #if the token is not in session then get the user to authenticate it
    if 'refresh_token' not in session: 
        return redirect('/api/auth/login')
    
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


#get the spotify profile of a user
def getUserProfile():

    #basic authentication
    if not ('access_token' in session):
        return redirect('/api/auth/login')
        
    #check refresh token
    if session['expires_at'] < datetime.now().timestamp():
        return redirect('api/spotify/refresh-token')
        
    #check header
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }
    profileInfo = []
    profileURL = API_BASE_URL + '/me'
    
    try:
        profile = requests.get(profileURL, headers=headers)
        profile = profile.json()
        profileInfo.append({
        "spotifyUserName": profile['display_name'],
        "linkToProfile":profile['external_urls']['spotify'],
        "spotifyId":profile['id'],
        "profilePicture": profile['images'][1]['url'],
        })
        return jsonify(profileInfo)
    except Exception:
        return make_response(jsonify({'error': 'Server Error'}), 401)
    

#a function to get the top songs
def getTopSongs() -> dict:
    #basic authentication
    if 'access_token' not in session:
        return redirect('/api/auth/login')
        
    #check refresh token
    if session['expires_at'] < datetime.now().timestamp():
        return redirect('api/spotify/refresh-token')
        
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
                topSongsInfo.append({
                    "id": song['id'],
                    "name": song['name'],
                    "popularity": float(song['popularity']), #how popular the song is on a scale of 0-100
                    "cover_image":  song['album']['images'][0]['url'],
                    "release_date": str(song['album']['release_date']),
                    "artists": currentArtistArray,
                    "song_link":  song['external_urls']['spotify'],
                })
                #make the array empty for the next song 
                currentArtistArray = []
        return jsonify(topSongsInfo)
    except Exception:
        return make_response(jsonify({'error': Exception}), 401)


def getRecentlyPlayed():
    userInfo = json.dumps(session['userInfo'])
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
        #all song ids
        songIds = ""
        
        #popularity average
        popularityAvg = 0
        
        #where we store the recent songs
        recentSongsInfo = []
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
                    
                recentSongsInfo.append(
                    {
                    #collect needed info respective variables
                    "id": song['id'],
                    "song_name":  song['name'],
                    "cover_images": song['album']['images'][0]['url'],
                    "artists": currentArtistArray,
                    "song_link":   song['external_urls']['spotify'],
                    }
                )
                popularityAvg += song['popularity']
                
                
                songIds += song['id'] + ","

                #make the array empty for the next song 
                currentArtistArray = []
        popularityAvg /= 50
        recentAnalysis = analyzeSongs(songIds)
        recentAnalysis.append(popularityAvg)
        return make_response(jsonify({'analysis': recentAnalysis, 'recents': recentSongsInfo}), 200)
    except Exception:
        return make_response(jsonify({'error': 'Unable to add recent songs'}), 401)

        

    
#get the top artists    
def getTopArtist():
    userInfo = str(session['userInfo'])
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
        allGenres = []
        #set the artists array to be -
        userTopArtistsInfo = []
        for artist in topArtists:
            if artist:
                userTopArtistsInfo.append(
                {              
                "name": artist['name'],
                "id":  artist['id'],
                "genres": artist['genres'],
                "images":  artist['images'][0]['url'],
                "popularity":  artist['popularity'],
                "artists_link":  artist['external_urls']['spotify'],
                })
                
                
                for genre in artist['genres']:
                    allGenres.append(genre)
                    
        #give back the array of dict with info
        return userTopArtistsInfo, allGenres
    except Exception:
        return make_response(jsonify({'error': 'Successfully added song to DB!'}), 401)

    



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
            #print session info:
            
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
                    if len(item['images']) > 0:
                        coverImage = item['images'][0]['url']
                    else:
                        coverImage = ""
                        
                    playlistInfo.append({
                        #add the important info their respective variables
                        "id": item['id'],
                        "playlist_name":  item['name'],
                        "playlist_link" :item['external_urls']['spotify'],
                        "cover_image": coverImage,
                        "spotify_link": item['tracks']['href']
                    })
                    
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
        make_response(jsonify({'error': Exception}))

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
    
        
        
        totalTracks = results['total']
        #we only want the items object
        tracksInfo = results['items']
        
        
        #arrays that will hold all the info
        allArtists = []
        allSongs = []
        
        #store the songIds in a string for the track analysis
        songIds = ""
        
        #save the artists for a song in a single string (this is because of SQL not allowing multi-deminsonal arrays of different sizes)
        artistForSong = []
        #info for all songs
        songsInfo = []
        #count is 0
        count = 0
        
        
        #loop through every track
        for index, item in enumerate(tracksInfo):
            #take the song title
            title = item['track']['name']
            #take the name of the artist
            artists =  item['track']['album']['artists']
            artistForSong = []
            #if someone has custom songs in their playlsit the code will crash so we are avoiding it by adding a try catch around it
            try:
                #ids, links, and image are only found for songs form the spotify app
                id = item['track']['id']
                link = item['track']['external_urls']['spotify']
                image = item['track']['album']['images'][0]['url']

            except:
                #custom song so just make the link for it empty
                link = ""
                image=""
                id =""

            #loop through the artist
            for artist in artists:
                artistForSong.append(artist['name'])
            songsInfo.append(
                {
                    "artist": artistForSong,
                    "link": link,
                    "title": title,
                    "id": id,
                    "image": image
                }
            )

            #for the first 100 songs of the playlist check add their song id
            if count < 100:
                #if the id is empty then we don't want spotify analyzing it because that will cause an error
                if id != "":  
                    if count != 0:
                        #get the ID
                        songIds += ',' + id
                    else:
                        songIds = id
                    count += 1
        #get the track features of a song
        trackFeatures = analyzeSongs(songIds)
        
        #put all the song info into a dict 
        allSongsInfo = {
            "song-data": songsInfo,
            "stats": trackFeatures,
            "total-tracks": totalTracks
        }
        return allSongsInfo
    except Exception:
        return make_response(jsonify({'error': 'Unable to access Playlist Info'}), 401)
    #return the dictionary 

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
    energyAvg = 0
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
            energyAvg += song['energy']

        #make songIds into an array then get its length to find num of songs
        numberOfSongs = len(songIds.split(','))
        
        #calc valence and dancebility of playlist
        valenceAvg = valenceAvg / numberOfSongs
        dancebilityAvg = dancebilityAvg / numberOfSongs

        #add this to an array 
        songFeaturesInfo = [valenceAvg, dancebilityAvg, energyAvg]
        #return the info
        return songFeaturesInfo
    
    except Exception: 
        return Response("API ERROR", status=401)

#controller function to call the API to add a playlist
def addPlaylist(playlistID: str):
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
        addPlaylistEndpoint = API_BASE_URL + '/playlist/' + playlistID + '/followers'
        #send request to follow a playlist, this doesn't return anything
        requests.put(addPlaylistEndpoint, headers=headers)
        return make_response(jsonify({'message': 'Successfully Followed Playlist'}), 200)
    except Exception:
        return make_response(jsonify({'error': 'Could not follow playlist'}), 401)

    
def addUser(userID: str):
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
        addUserEndpoint = API_BASE_URL + f'/following?ids={userID}'
        requests.put(addUserEndpoint, headers=headers)
        return make_response(jsonify({'message': 'Successfully Followed User'}), 200)
    except Exception:
        return make_response(jsonify({'error': 'Could not Follow User'}), 401)


#return an array of all the top artists 
def getTopArtistsStrings(artists: list[dict]) -> (str, str, str, str, str):
    name = ""
    artists_id = ""
    genres = ""
    images = ""
    popularity = ""
    artists_link = ""
    
    for artist in artists:
        name += "**" + artist['name']
        artists_id += "**" + artist['id']
        genres += "**" + '&&'.join(artist['genres'])
        images += "**" + artist['images']
        popularity += "**" + str(artist['popularity'])
        artists_link += "**" + artist['artists_link']
    return artists_id, name, genres, images, artists_link, popularity

def getTopSongsStrings(songs: list[dict]):
    song_id = ""
    song_name = ""
    song_artists = ""
    song_link = ""
    popularity = ""
    release_date = ""
    cover_image = ""
    for song in songs:

        song_id += "**" + song['id']
        song_name += "**" + song['name']
        popularity += "**" +  str(song['popularity']) #how popular the song is on a scale of 0-100
        cover_image  += "**" + song["cover_image"]
        release_date += "**" + song['release_date']
        song_artists += "**" + '&&'.join(song['artists'])
        song_link +="**" + song['song_link']
    return song_id, song_name, song_artists, song_link, popularity, release_date, cover_image

def getRecentSongs(recents: list[dict]):
    song_id = ""
    song_name = ""
    artist_name = ""
    song_link = ""
    cover_image = ""
    for song in recents:
        #collect needed info respective variables
        song_id += "**" + str(song['id'])
        song_name  +=  "**" +  song['song_name']
        artist_name += "**" +  '&&'.join(song['artists'])
        cover_image +=   "**" +  song['cover_images']
        song_link +=  "**" +  song['song_link']
    return song_id, song_name, artist_name, cover_image, song_link

def getSpotifyProfileStats(profile: list[dict], stats: dict):
    spotifyUserName = profile['spotifyUserName']
    linkToProfile = profile['linkToProfile']
    spotifyId = profile['spotifyId']
    profilePicture = profile['profilePicture']
    recentValence = stats[0]
    recentDanceability = stats[1]
    recentEnergy = stats[2]
    recentPopularity = stats[3]
    return spotifyUserName, linkToProfile, spotifyId, profilePicture, recentValence, recentDanceability, recentEnergy, recentPopularity

def getPlaylist(playlists: list[dict]):
    playlist_id = ""
    playlist_name = ""
    playlist_link = ""
    playlist_cover = ""
    for playlist in playlists:
        playlist_id += "**" + playlist['id']
        playlist_name += "**" + playlist['playlist_name']
        playlist_link += "**" + playlist['playlist_link']
        playlist_cover += "**" + playlist['cover_image']
    
    return playlist_id, playlist_name, playlist_link, playlist_cover

def addToDB(songs, artists, recent, profile, stats, playlist):
    try:
        with connection:
            with connection.cursor() as cursor:
                
                existsQuerry = CHECK_IF_ALREADY_ADDED.format('spotify_profile', 'spotify_profile_token')
                cursor.execute(existsQuerry, (session['userInfo'],))
                exists = cursor.fetchall()

                artistsVars = getTopArtistsStrings(artists)
                songVars = getTopSongsStrings(songs)
                recentSongsVars = getRecentSongs(recent)
                profileVars = getSpotifyProfileStats(profile, stats)
                playlistVars = getPlaylist(playlist)
                if exists:
                    cursor.execute(UPDATE_TOP_ARTISTS, (artistsVars[0], artistsVars[1], artistsVars[2], artistsVars[3], artistsVars[4], artistsVars[5], session['userInfo'],))
                    cursor.execute(UPDATE_TOP_SONGS, (songVars[0], songVars[1], songVars[2], songVars[3], songVars[4], songVars[5], songVars[6], session['userInfo'],))
                    cursor.execute(UPDATE_SPOTIFY_PROFILE, (profileVars[0], profileVars[1], profileVars[2], profileVars[3], profileVars[4], profileVars[5], profileVars[6], profileVars[7], session['userInfo'],))
                    cursor.execute(UPDATE_PLAYLISTS, (playlistVars[0], playlistVars[1], playlistVars[2], playlistVars[3], session['userInfo'],))
                    cursor.execute(UPDATE_RECENT_SONGS, (recentSongsVars[0], recentSongsVars[1], recentSongsVars[2], recentSongsVars[3], recentSongsVars[4], session['userInfo'],))
                else:  
                    cursor.execute(INSERT_TOP_ARTISTS, (artistsVars[0], artistsVars[1], artistsVars[2], artistsVars[3], artistsVars[4], artistsVars[5], session['userInfo'],))
                    cursor.execute(INSERT_TOP_SONGS, (songVars[0], songVars[1], songVars[2], songVars[3], songVars[4], songVars[5], songVars[6], session['userInfo'],))
                    cursor.execute(INSERT_RECENT_SONGS, (recentSongsVars[0], recentSongsVars[1], recentSongsVars[2], recentSongsVars[3], recentSongsVars[4], session['userInfo'],))
                    cursor.execute(INSERT_SPOTIFY_PROFILE, (profileVars[0], profileVars[1], profileVars[2], profileVars[3], profileVars[4], profileVars[5], profileVars[6], profileVars[7], session['userInfo']))
                    cursor.execute(INSERT_PLAYLISTS, (playlistVars[0], playlistVars[1], playlistVars[2], playlistVars[3], session['userInfo'],))
        connection.commit()
        return make_response(jsonify({'message': 'Updated Database!'}), 200)

    except Exception:
        return make_response(jsonify({'error': 'Could not update databse'}), 401)
 
def getSearchResults(searchTerms: str) -> json:
    query = ""
    resultsDict = {}
    resultTokens = []
    allTokens = []
    favouriteArtists = {}
    favouriteSong = {}
  
    
    with connection:
        with connection.cursor(cursor_factory=extras.DictCursor) as cursor:
            for search in searchTerms:
                #Make the query have '%' around it to make it a wildcard
                query = "%" + search.strip().title() + "%"
                print(query)
                cursor.execute(FIND_INSTANCE_OF_IN_TOP_SONGS, (query, query,))
                for index, row in enumerate(cursor.fetchall()):
                    if row['top_songs_token'] != session['userInfo']:
                        artistName = row['artists_name'].split("**")[1]
                        artistName = artistName.split(",")
                        favouriteSong[row['top_songs_token']] = [row['song_name'].split("**")[1], artistName]
                        resultsDict[row['top_songs_token']] =  1 + resultsDict[row['top_songs_token']] if row['top_songs_token'] in resultsDict else 1
                        
                cursor.execute(FIND_INSTANCE_OF_IN_TOP_ARTISTS, (query,))
                for index, row in enumerate(cursor.fetchall()):
                    if row['top_artists_token'] != session['userInfo']:
                        resultsDict[row['top_artists_token']] =  1 + resultsDict[row['top_artists_token']] if row['top_artists_token'] in resultsDict else 1


                cursor.execute(FIND_INSTANCE_OF_IN_RECENT_SONGS, (query, query,))
                for index, row in enumerate(cursor.fetchall()):
                    if row['recent_songs_token'] != session['userInfo']:
                        resultsDict[row['recent_songs_token']] =  1 + resultsDict[row['recent_songs_token']] if row['recent_songs_token'] in resultsDict else 1

            for token, count in resultsDict.items():
                cursor.execute(GET_FAV_SONG_AND_ARTISTS_PREVIEW, (token,))
                results = cursor.fetchone()
                favouriteArtists[token] = results['top_artists_name'].split("**")[1:4]
                favouriteSong[token] = [results['top_song_name'].split("**")[1], results['top_song_artist'].split("**")[1].split(",")]
                resultTokens.append([token, count])
                
            sortedResults = sorted(resultTokens, key=lambda x: x[1], reverse=True)
            displayResultsList = []
            for result in sortedResults:
                cursor.execute(FIND_PROFILE, (result[0],))
                user = cursor.fetchone()
                compatability = analyzeCompatibility(len(searchTerms), result)
                displayResultsList.append({
                    'username': user['display_name'],
                    'id': user['spotify_id'],
                    'profile-picture': user['profile_picture'],
                    'score': compatability,
                    'favourite-artists': favouriteArtists[result[0]],
                    'favourite-songs': favouriteSong[result[0]],
                    'link': user['link_to_profile'],
                    'token': result[0]
                })
        connection.commit()
    return displayResultsList

    
def analyzeCompatibility(terms: int, result: list[str, int]) -> int:
    return int((result[1]/(terms*3))*100)

def getInfoForProfile(token: str):
    topSongsInfo = []
    topArtistsInfo = []
    recentSongsInfo = []
    artistArray = []
    playlistInfo = []
    genresArray = []
    allGenres = []
    profileInfo = []
    spotifyStats = []
    allInfo = {}
    with connection:
        with connection.cursor(cursor_factory=extras.DictCursor) as cursor:
            #using SQL join to get all the info relating to a certain user by their token
            cursor.execute(GET_ALL_INFO, (token,))
            #fetching the result (should only be one)
            results = cursor.fetchone()
            
            #****TOP SONGS*****
            #getting the artists for the top artists in a good format
            for artist in results['top_songs_artist'].split("**")[1:]:
                artistArray.append(artist.split("&&"))
            
            #setting all variables accordingly for topsongs
            cover_image  =results['top_songs_image'].split("**")[1:]
            name = results['top_songs_name'].split("**")[1:]
            artists = artistArray
            song_link = results["top_songs_link"].split("**")[1:]
            
            #adding all top songs to an array with dictionary
            for i in range(len(song_link)):
                topSongsInfo.append(
                    {
                        "cover_image": cover_image[i],
                        "name": name[i],
                        "artists": artists[i],
                        "song_link": song_link[i]
                    }
                )
            artistArray = []
            #****TOP ARTISTS*****
            #getting top genres for each artist
            for genre in results['top_artists_genres'].split("**")[1:]:
                genresArray.append(genre.split("&&"))
            
            #setting all variables accordinglu
            cover_image = results['top_artists_image'].split("**")[1:]
            name = results['top_artists_name'].split("**")[1:]
            artist_link = results['top_artists_link'].split("**")[1:]
            for i in range(len(song_link)):
                topArtistsInfo.append(
                    {
                        "images": cover_image[i],
                        "name": name[i],
                        "genres": genresArray[i],
                        "artists_link": artist_link[i]
                    }
                )
                for genre in genresArray[i]:
                    allGenres.append(genre)
                    
            #***RECENT SONGS****
            cover_image = results['recent_songs_images'].split("**")[1:]
            name = results['recent_songs_name'].split("**")[1:]
            song_link = results['recent_songs_link'].split("**")[1:]
            
            for artists in results['recent_songs_artists'].split("**")[1:]:
                artistArray.append(artists.split("&&"))
            for i in range(len(song_link)):
                recentSongsInfo.append(
                    {
                        "cover_images": song_link[i],
                        "song_name": name[i],
                        "artists": artistArray[i],
                        "song_link": cover_image[i]
                    }
                )
            
            #***PROFILE INFO***
            spotifyUserName = results['spotify_name']
            profilePicture = results['spotify_profile_picture']
            profileInfo.append({
                "spotifyUserName": spotifyUserName,
                "profilePicture": profilePicture
            })
            #STATS INFO 
            #add each part to an array
            spotifyStats.append(results['spotify_valence'])
            spotifyStats.append(results['spotify_energy'])
            spotifyStats.append(results['spotify_danceability'])
            spotifyStats.append(results['spotify_popularity'])
            
            playlist_name = results['playlist_name'].split("**")[1:]
            playlist_id = results['playlist_id'].split("**")[1:]
            playlist_cover = results['playlist_cover'].split("**")[1:]
            
            for i in range(len(playlist_name)):
                playlistInfo.append(
                    {
                        "id": playlist_id[i],
                        "playlist_name": playlist_name[i],
                        "cover_image": playlist_cover[i]
                    }
                )

            
    allInfo["top-songs"] = topSongsInfo
    allInfo["top-artists"] = topArtistsInfo
    allInfo["top-genres"] = allGenres
    allInfo["top-artists"] = topArtistsInfo
    allInfo['recent-songs'] = recentSongsInfo
    allInfo['profile']  = profileInfo
    allInfo['stats'] = spotifyStats
    allInfo["playlist"] = playlistInfo
    return allInfo
    return make_response(jsonify({'error': 'temp message'}), 401)



  
    
        
        
    