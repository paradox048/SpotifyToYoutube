import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth  
from dotenv import load_dotenv

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
    songs = []
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.load_songs()
        
    
    def load_songs(self):
        results = sp.playlist_items(self.id)
        for song in results['items']:
            self.songs.append(song['track']['name'])
        
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def get_songs(self):
        return self.songs
    
    def __str__(self):
        return f"Playlist Name: {self.name}\nPlaylist ID: {self.id}\n"

    

load_dotenv()

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

# Iterate and print playlist names and IDs
for playlists in user_playlists['items']:
    playlist_list.append(playlist(playlists['name'], playlists['id']))

# Print playlist names and IDs
for playlist in playlist_list:
    print(playlist)
    #print(playlist.get_songs())
    print("-------------")





    

