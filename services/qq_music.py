import requests
from bridge.reply import Reply, ReplyType
from bridge.context import ContextType


class QQMusicService:
    def __init__(self, base_url="https://c.y.qq.com"):
        self.base_url = base_url

    def search_song(self, keyword):
        """搜索 QQ 音乐歌曲"""
        search_url = f"{self.base_url}/soso/fcgi-bin/client_search_cp"
        params = {
            "w": keyword,
            "format": "json",
            "n": 1,  # 返回一条结果
        }
        try:
            response = requests.get(search_url, params=params)
            data = response.json()

            if "data" in data and "song" in data["data"]:
                song = data["data"]["song"]["list"][0]
                song_id = song["songmid"]
                share_url = self.get_song_share_url(song_id)  # 获取分享链接

                return {
                    "name": song["songname"],
                    "artist": song["singer"][0]["name"],
                    "url": share_url,  # 分享链接
                    "cover": f"https://y.qq.com/music/photo_new/T002R300x300M000{song['albummid']}.jpg",  # 封面图片
                }
        except Exception as e:
            print(f"Error searching song: {e}")
        return None

    def get_song_share_url(self, song_id):
        """通过歌曲 ID 获取分享播放链接"""
        share_url_api = f"{self.base_url}/song/fcgi-bin/fcg_get_song_info.fcg"
        params = {
            "songmid": song_id,
            "format": "json",
        }
        try:
            response = requests.get(share_url_api, params=params)
            data = response.json()
            if "url" in data:
                return data["url"]  # 返回分享链接
        except Exception as e:
            print(f"Error fetching share link: {e}")
        return None


class QQMusicPlugin:
    def __init__(self):
        self.qq_music_service = QQMusicService()

    def handle_context(self, e_context):
        if e_context["context"].type != ContextType.TEXT:
            return

        content = e_context["context"].content.strip()
        if not content.startswith("点歌"):
            return

        # 提取关键词
        keyword = content[2:].strip()
        if not keyword:
            e_context["reply"] = Reply(ReplyType.INFO, "请输入歌曲关键词，例如：点歌 稻香")
            return

        # 搜索歌曲
        result = self.qq_music_service.search_song(keyword)
        if result:
            card_message = {
                "msgtype": "news",
                "news": {
                    "articles": [
                        {
                            "title": result["name"],
                            "description": result["artist"],
                            "url": result["url"],  # 分享链接
                            "picurl": result["cover"],  # 封面图片
                        }
                    ]
                }
            }
            e_context["reply"] = Reply(ReplyType.CARD, card_message)
        else:
            e_context["reply"] = Reply(ReplyType.INFO, "未找到相关歌曲，请尝试其他关键词。")