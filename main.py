import spotipy
import os
from pytube import YouTube
from spotipy.oauth2 import SpotifyOAuth  
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#stores playlist name and id
class song(object):
    def __init__(self, name, id, artist):
        self.name = name
        self.id = id
        self.artist = artist
        
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def get_artist(self):
        return self.artist
    
    def __str__(self):
        return f"Song Name: {self.name}\nSong ID: {self.id}\nSong Artist: {self.artist}\n"
    
class playlist(object):
    
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.songs = []
        self.load_songs()
        
    def load_songs(self):
        results = sp.playlist_items(self.id)
        for track in results['items']:
            song_obj = song(track['track']['name'], track['track']['id'], track['track']['artists'][0]['name'])
            self.songs.append(song_obj)
        
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def get_songs(self):
        str = ""
        for song in self.songs:
            str += song.__str__()
        return str
    
    def __str__(self):
        return f"Playlist Name: {self.name}\nPlaylist ID: {self.id}\n"

    
# Load environment variables
load_dotenv()

#Google
API_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

#Spotify
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECR")
REDIRECT_URI = os.getenv("REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="user-library-read"))

# Get user's playlists
user_playlists = sp.current_user_playlists()
playlist_list = []

#store playlist list
for playlists in user_playlists['items']:
    playlist_list.append(playlist(playlists['name'], playlists['id']))


print("Choose a playlist to convert to youtube: ")
for i in range(len(playlist_list)):
    print(f"{i+1}. {playlist_list[i].get_name()}")
    
user_input = int(input("Enter a number: "))


# Google API
creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
      
youtube = build('youtube', 'v3', credentials=creds)

# Create the playlist
playlist_title = playlist_list[user_input-1].get_name()
playlist_description = f"Converted from Spotify playlist: {playlist_title}"
request = youtube.playlists().insert(
    part='snippet,status',
    body={
        'snippet': {
            'title': playlist_title,
            'description': playlist_description
        },
        'status': {
            'privacyStatus': 'public'  # Adjust privacy status as needed
        }
    }
)

# Execute the request
response = request.execute()
playlist_id = response['id']

#load up songs from spotify to youtube playlist
for song in playlist_list[user_input-1].songs:
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=song.get_name() + " " + song.get_artist()
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": playlist_id,
            "position": 0,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": video_id
            }
          }
        }
    )
    response = request.execute()
    print(f"Added {song.get_name()} to playlist")
    
print("Playlist created successfully!")
print("Would you like to download the playlist? (y/n)")
user_input = input("Enter a letter: ")

#use pytube to download playlist
#grab the playlist id from the url
playlist_id = playlist_id[2:]
print(playlist_id)



