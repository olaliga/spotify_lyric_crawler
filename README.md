# spotify_lyric_crwler
spotify_lyric_crwler 會從魔境歌詞網中抓取 Spotify 播放清單中的中文歌曲的歌詞

但你需要先去以下網址註冊 Spotify api 獲得 CLIENT_ID, CLIENT_SECRET 並且設定當中 redirect url
https://developer.spotify.com/dashboard/

此程式需要 6 個參數：

    USERNAME : spotify 使用者名稱

    SPOTIPY_CLIENT_ID : spotify api 中所提供的 CLIENT_ID

    SPOTIPY_CLIENT_SECRET : spotify api 中所提供的 CLIENT_SECRET

    file_name = 下載檔案的自訂名稱

    redirect_url = spotify api 中所設定的 redirect_url

    playlist = spotify 中的播放清單

    
usage : 

    python3 main.py USERNAME SPOTIPY_CLIENT_ID SPOTIPY_CLIENT_SECRET file_name redirect_url playlist
    
抓取的歌詞資訊以及歌詞會在 download_data 資料夾中存成 json 檔
