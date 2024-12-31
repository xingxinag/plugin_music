import requests

class NeteaseMusicService:
    def __init__(self, config):
        self.api_url = config.get("api_url", "")

    def search_song(self, keyword):
        """通过关键词搜索网易云音乐的歌曲"""
        try:
            params = {
                "s": keyword,  # 搜索关键字
                "type": 1,     # 搜索类型：1 表示单曲
                "offset": 0,   # 偏移量
                "limit": 1     # 返回数量，1 表示只返回第一首歌
            }
            headers = {
                "Referer": "https://music.163.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.post(self.api_url, data=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # 解析返回结果，提取第一首歌曲信息
            song_list = data.get("result", {}).get("songs", [])
            if not song_list:
                return None

            song = song_list[0]
            song_id = song["id"]
            song_name = song["name"]
            singer_name = ", ".join([artist["name"] for artist in song["artists"]])

            # 拼接卡片分享链接
            card_url = f"https://music.163.com/song?id={song_id}"

            return {
                "name": song_name,
                "artist": singer_name,
                "url": card_url
            }
        except requests.exceptions.RequestException as e:
            print(f"Error searching song: {e}")
        return None