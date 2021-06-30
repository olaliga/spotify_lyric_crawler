import spotify_songname_crawler as songname
import lyric
from tqdm import tqdm
import numpy as np
from time import sleep
import json, os, requests, time, itertools


def get_song_attributes(response_text):
    return json.loads(response_text)

def artist_chinese_dict(crawler):
    artists = crawler.artists
    print("Crawler artists chinese name.")
    artists_dict = {}
    artists_unique = np.unique(np.array(list(itertools.chain(*artists)), dtype=object))

    for item in tqdm(artists_unique):
        artists_dict[item] = lyric.search_singer(item)

    return artists_dict

def update_artist_chinese_dict(update_chinese_dict, artists_dict):
    i = 0
    for item in update_chinese_dict.keys():
        artists_dict[item] = update_chinese_dict[item]
        i = i + 1
    return artists_dict


class song_dict():
    def __init__(self, playlist, song_type, update_chinese_dict, update_song_dict, USERNAME, SCOPE, headers):
        self.playlist = playlist
        self.song_type = song_type
        self.update_chinese_dict = update_chinese_dict
        self.update_song_dict = update_song_dict
        self.artists_dict = {}
        self.song_dict = {}
        self.USERNAME = USERNAME
        self.SCOPE = SCOPE
        self.headers = headers

    def song_dict_crawler(self):
        print("Spotify Playlist Crawler : ")
        crawler = songname.crawler(playlist=self.playlist, USERNAME=self.USERNAME,
                                   SCOPE = self.SCOPE, headers = self.headers)
        crawler.startcrawl()
        songnames = crawler.songnames

        self.artists_dict = artist_chinese_dict(crawler)
        self.artists_dict = update_artist_chinese_dict(self.update_chinese_dict, self.artists_dict)

        search_data = crawler.myjson_data
        search_dict = {}
        for search in search_data:
            need = []
            for item in search['track']['artists']:
                need.append(item['name'])

            for i in need:
                if i in search_dict.keys():
                    search_dict[i].append(search['track']['name'])
                else:
                    search_dict[i] = []
                    search_dict[i].append(search['track']['name'])

        print("Construct Song dict")
        i = 0
        for search in tqdm(search_data):
            i = i + 1
            if i % 100 == 0:
                sleep(7)
            song = search['track']['name']

            if song in self.update_song_dict.keys():
                song = self.update_song_dict[song]
            song_ids = search['track']['uri'].split(':')[2]

            song_attributes = requests.get(f"https://api.spotify.com/v1/audio-features/{song_ids}", headers = self.headers)

            mood = get_song_attributes(song_attributes.text)['valence']
            danceability = get_song_attributes(song_attributes.text)['danceability']
            energy = get_song_attributes(song_attributes.text)['energy']
            key = get_song_attributes(song_attributes.text)['key']
            loudness = get_song_attributes(song_attributes.text)['loudness']
            mode = get_song_attributes(song_attributes.text)['mode']
            speechiness = get_song_attributes(song_attributes.text)["speechiness"]
            acousticness =  get_song_attributes(song_attributes.text)["acousticness"]
            instrumentalness = get_song_attributes(song_attributes.text)["instrumentalness"]
            liveness = get_song_attributes(song_attributes.text)["liveness"]
            tempo = get_song_attributes(song_attributes.text)["tempo"]


            need = []
            need2 = []
            for item in search['track']['artists']:
                need.append(item['name'])
                need2.append(self.artists_dict[item['name']])
            self.song_dict[song] = {'artists': need,
                               'artists_chinese_name': need2,
                               'Type': self.song_type,
                               'moode': mood,
                                'danceability': danceability,
                                'energy ':energy ,
                                'key' : key,
                                'loudness':loudness,
                                'mode':mode,
                                'speechiness':speechiness,
                                'acousticness':acousticness,
                                'instrumentalness':instrumentalness,
                                'liveness':liveness,
                                'tempo':tempo
                               }
        time_1 = time.time()
        print("Crawl the lyric")


        for i in range(len(songnames)):
            if songnames[i] in self.update_song_dict.keys():
                songnames[i] = self.update_song_dict[songnames[i]]

        for item in tqdm(songnames):
            lyric_search = lyric.search_song(item)
            if len(lyric_search) != 0:
                k = 0
                keep = True
                while keep:
                    if k >= len(lyric_search):
                        self.song_dict[item]['lyric_url'] = False
                        self.song_dict[item]['lyric'] = False
                        keep = False
                    else:
                        dum = lyric_search[k]
                        if dum['singer'] in "".join(
                                self.song_dict[item]['artists_chinese_name']):  ### fix : chinese name in detail
                            # print(dum['singer'])
                            keep = False
                            lyric_url = lyric_search[k]['link']
                            self.song_dict[item]['lyric_url'] = lyric_url
                            self.song_dict[item]['lyric'] = lyric.get_lyric(lyric_url)
                    k = k + 1
                    # print(k)
            else:
                self.song_dict[item]['lyric_url'] = False
                self.song_dict[item]['lyric'] = False

        time_lyric_crawler = time.time() - time_1
        print("Lyric Crawler : " + str(time_lyric_crawler))

