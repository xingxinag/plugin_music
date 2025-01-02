import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests

class QQMusicService:
    def __init__(self, config):
        self.base_url = config.get("api_url", "https://c.y.qq.com")
        self.cover_url_template = "https://y.qq.com/music/photo_new/T002R300x300M000{0}.jpg"

    def search_song(self, keyword):
        try:
            params = {
                "ct": 24,
                "qqmusic_ver": 1298,
                "remoteplace": "txt.yqq.song",
                "searchid": "64404621762404874",
                "aggr": 1,
                "catZhida": 1,
                "lossless": 0,
                "sem": 1,
                "t": 0,
                "p": 1,
                "n": 1,
                "w": keyword,
                "platform": "yqq",
                "format": "json"
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if "data" not in data or "song" not in data["data"] or "list" not in data["data"]["song"]:
                return {"error": True, "message": "未找到相关歌曲，请尝试其他关键词。"}

            song_list = data["data"]["song"]["list"]
            if not song_list:
                return {"error": True, "message": "未找到相关歌曲，请尝试其他关键词。"}

            song = song_list[0]
            song_name = song.get("songname", "未知歌曲")
            singer = song["singer"][0]["name"] if song.get("singer") else "未知歌手"
            song_mid = song.get("songmid", "")
            album_mid = song.get("albummid", "")

            share_link = f"https://i.y.qq.com/v8/playsong.html?songmid={song_mid}&ADTAG=ryqq.songDetail"
            cover_url = self.cover_url_template.format(album_mid) if album_mid else "https://y.qq.com/default_cover.jpg"

            return {
                "error": False,
                "data": {
                    "name": song_name,
                    "artist": singer,
                    "url": share_link,
                    "cover": cover_url
                }
            }
        except Exception as e:
            return {"error": True, "message": f"搜索歌曲时出错：{str(e)}"}