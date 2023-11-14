import os
from dotenv import load_dotenv

#setup the .env file
load_dotenv()

#Spotify API information
API_INFORMATION = []

#getting secret info API_INFORMATION
API_INFORMATION.append(os.getenv("CLIENT_ID"))
API_INFORMATION.append(os.getenv("CLIENT_SECRET"))
API_INFORMATION.append(os.getenv("REDIRECT_URI"))
print(API_INFORMATION[2])

#important spotify urls 
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1'

