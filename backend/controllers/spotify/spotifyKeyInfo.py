import os
from dotenv import load_dotenv

#setup the .env file
load_dotenv()

#Spotify API information
API_INFORMATION = []

print("hope this works", os.getenv('CLIENT_ID'))

#getting secret info API_INFORMATION
API_INFORMATION.append(os.getenv("CLIENT_ID2"))
API_INFORMATION.append(os.getenv("CLIENT_SECRET2"))
API_INFORMATION.append(os.getenv("REDIRECT_URI"))

#important spotify urls 
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1'

