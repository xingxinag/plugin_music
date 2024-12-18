import json
from services.qq_music import QQMusicService
from services.netease_music import NeteaseMusicService
from services.kugou_music import KugouMusicService

class MusicPlugin:
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.services = {
            "qq": QQMusicService(config['qq_music']),
            "netease": NeteaseMusicService(config['netease_music']),
            "kugou": KugouMusicService(config['kugou_music'])
        }

    def search_song(self, platform, keyword):
        if platform in self.services:
            return self.services[platform].search_song(keyword)
        else:
            return f"Unsupported platform: {platform}"

    def get_song_url(self, platform, song_id):
        if platform in self.services:
            return self.services[platform].get_song_url(song_id)
        else:
            return f"Unsupported platform: {platform}"