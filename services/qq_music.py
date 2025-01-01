import requests

class QQMusic:
    def __init__(self):
        self.base_url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
        self.cover_url_template = "https://y.qq.com/music/photo_new/T002R300x300M000{0}.jpg"

    def search_music(self, keyword):
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
            data = response.json()
            
            if "data" not in data or "song" not in data["data"] or "list" not in data["data"]["song"]:
                return "[INFO]\n未找到相关歌曲，请尝试其他关键词。"

            song_list = data["data"]["song"]["list"]
            if not song_list:
                return "[INFO]\n未找到相关歌曲，请尝试其他关键词。"

            song = song_list[0]
            song_name = song.get("songname", "未知歌曲")
            singer = song["singer"][0]["name"] if song.get("singer") else "未知歌手"
            song_mid = song.get("songmid", "")
            album_mid = song.get("albummid", "")

            # 使用新链接格式
            share_link = f"https://i.y.qq.com/v8/playsong.html?songmid={song_mid}&ADTAG=ryqq.songDetail"
            cover_url = self.cover_url_template.format(album_mid)
            card_message = self.generate_card(song_name, singer, cover_url, share_link)

            return card_message

        except Exception as e:
            return f"[ERROR]\n搜索歌曲时出错：{str(e)}"

    def generate_card(self, song_name, singer, cover_url, share_link):
        return {
            "title": song_name,
            "description": singer,
            "url": share_link,
            "thumb_url": cover_url
        }

# 测试代码
if __name__ == "__main__":
    qq_music = QQMusic()
    keyword = "知我"
    result = qq_music.search_music(keyword)
    print(result)