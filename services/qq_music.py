import requests
import urllib.parse

class QQMusicService:
    def __init__(self, config):
        self.api_url = config.get("api_url", "")

    def search_song(self, keyword):
        """通过关键词搜索歌曲"""
        try:
            params = {
                "w": keyword,  # 搜索关键字
                "format": "json",  # 返回 JSON 格式
                "p": 1,  # 页码
                "n": 1  # 返回数量，1 表示只返回第一首歌
            }
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # 解析返回结果，提取第一首歌曲信息
            song_list = data.get("data", {}).get("song", {}).get("list", [])
            if not song_list:
                return None

            song = song_list[0]
            song_id = song["songmid"]
            song_name = song["songname"]
            singer_name = song["singer"][0]["name"]

            # 拼接卡片分享链接
            card_url = f"https://y.qq.com/n/ryqq/songDetail/{song_id}"

            return {
                "name": song_name,
                "artist": singer_name,
                "url": card_url
            }
        except requests.exceptions.RequestException as e:
            print(f"Error searching song: {e}")
        return None