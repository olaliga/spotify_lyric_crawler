import spotipy.util as util
import lyric_data as db
import os, json, sys


if __name__ == '__main__':

    if len(sys.argv) != 7:
        print('Missing argument or too much argument')
        sys.exit()

    USERNAME = sys.argv[1]
    os.environ['SPOTIPY_CLIENT_ID'] = sys.argv[2]
    os.environ['SPOTIPY_CLIENT_SECRET'] = sys.argv[3]
    file_name = sys.argv[4]
    redirect_uri = sys.argv[5]
    playlist = sys.argv[6]


    SCOPE = 'user-library-read'
    token = util.prompt_for_user_token(USERNAME, SCOPE,
                                       # 注意需要在自己的web app中添加redirect url
                                       redirect_uri = redirect_uri)
    headers = {"Authorization": "Bearer {}".format(token)}


    update_chinese_dict = {
        'ASi': '阿肆', 'A-Mei Chang': '張惠妹', 'A/DA 阿達': 'A/DA 阿達', 'Abin Fang': '方烱彬',
        'Aggie': 'Aggie', 'Aggie Hsieh': '謝沛恩', 'Alisa Galper': 'Alisa Galper', 'Ann Bai': '白安',
        'Aydo$': 'Aydo$', 'Ben': 'Ben', 'Bravex': 'Bravex', 'Hu Xia': '胡夏', 'JW': '王灝兒',
        'Jia Jia': '家家', 'LION': '獅子', 'Lulu': 'Lulu', 'Ren Ran': '任然', 'Rui En': 'Rui En',
        'Shi Shi': '孫盛希', 'Shin': '信', 'Young Gee': 'Young Gee', 'Shin-Ski': 'Shin-Ski', 'Ty.': 'Ty.'}

    update_song_dict = {'4:00A.M.' : '4:00+A.+M.'}

    playlist_data = db.song_dict(playlist=playlist, song_type='Indep',
                         update_chinese_dict=update_chinese_dict, update_song_dict = update_song_dict,
                                USERNAME = USERNAME, SCOPE = SCOPE, headers = headers)

    playlist_data.song_dict_crawler()

    dict = playlist_data.song_dict

    current_dir = os.getcwd()
    os.chdir('download_data')
    json.dump(dict, open(file_name+".json", 'w'))
    os.chdir(current_dir)
