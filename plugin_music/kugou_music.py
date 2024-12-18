import requests

class KugouMusicService:
    def __init__(self, config):
        self.api_url = config['api_url']

    def search_song(self, keyword):
        response = requests.get(f"{self.api_url}/search", params={"keyword": keyword})
        return response.json()

    def get_song_url(self, song_id):
        response = requests.get(f"{self.api_url}/song", params={"id": song_id})
        return response.json()