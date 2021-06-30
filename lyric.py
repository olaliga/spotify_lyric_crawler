import requests
import urllib.parse
import re
from bs4 import BeautifulSoup
import json


URL_ROOT = 'http://mojim.com/'

def search_song(song_name):
    song_name += '.html?t3'
    url = URL_ROOT+song_name
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    songs = soup.find_all('dd', re.compile('^mxsh_dd'))
    if len(songs) == 0:
        song_list = list()
    else:
        del songs[0]
        song_list = list()

        for song in songs:
            meta = song.find('span', 'mxsh_ss4').find('a')
            name_temp = meta.getText().split('.')
            song_list.append({
                'name': name_temp[1],
                'singer': song.find('span', 'mxsh_ss2').getText(),
                'album': song.find('span', 'mxsh_ss3').getText(),
                'link': meta.get('href'),
            })

    return song_list

def search_singer(singer):
    name = singer
    singer += '.html?t1'
    url = urllib.parse.urljoin(URL_ROOT, singer)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    search_list_exist = soup.find_all(['li'])
    if len(search_list_exist) > 0:
        search_list = soup.find_all(['li'])[0].find_all(["a"])
        singer_id = search_list[0].attrs['href']

        url = urllib.parse.urljoin(URL_ROOT, singer_id)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        inform = json.loads(soup.find_all(["div", 'script'], type="application/ld+json")[0].contents[0])
        singer_chinese_name = inform['itemListElement'][0]['name']
    else:
        singer_chinese_name = name
    return singer_chinese_name


def get_lyric(url):
    url = urllib.parse.urljoin(URL_ROOT, url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    lyric = soup.find('dl', 'fsZx1')

    a = re.compile('^\[\d+')

    lyric_list = list()
    for string in lyric.stripped_strings:
        if string == '更多更詳盡歌詞 在' or string == '※ Mojim.com　魔鏡歌詞網':
            continue
        if a.match(string):
            break
        lyric_list.append(string)

    singer = lyric_list.pop(0)
    name = lyric_list.pop(0)

    song_detail = {
        'singer': singer,
        'name': name,
        'lyric': lyric_list
    }
    return song_detail


