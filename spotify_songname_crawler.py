import random
import warnings
import spotipy

import os
import json
import spotipy.util as util
import requests
from time import sleep
from tqdm import tqdm


def get_song_attributes(response_text):
    return json.loads(response_text)

class crawler():
    def __init__(self,  playlist, USERNAME, SCOPE, headers):
        self.playlist = playlist
        self.USERNAME = USERNAME
        self.SCOPE = SCOPE
        ## addition need

        self.songnames = list()
        self.artists = list()
        self.mood = list()
        self.myjson_data = dict()
        self.headers = headers
        
    # crawl data
    def startcrawl(self):
        responses = requests.get("https://api.spotify.com/v1/playlists/" + self.playlist, headers = self.headers)
        crawler_data = json.loads(responses.text)['tracks']
        self.myjson_data = crawler_data['items']

        while crawler_data['next'] != None:
            responses = requests.get(crawler_data['next'], headers = self.headers)
            crawler_data = json.loads(responses.text)
            self.myjson_data = self.myjson_data + crawler_data['items']

        for i in range(len(self.myjson_data)):
            self.songnames.append(self.myjson_data[i]['track']['name'])
            need = []
            for j in range(len(self.myjson_data[i]['track']['artists'])):
                need.append(self.myjson_data[i]['track']['artists'][j]['name'])
            self.artists.append(need)
