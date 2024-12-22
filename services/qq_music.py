import requests

class QQMusicService:
    def __init__(self, config):
        self.api_url = config["api_url"]

    def search_song(self, keyword):
        try:
            response = requests.get(f"{self.api_url}/search", params={"keyword": keyword})
            response.raise_for_status()
            data = response.json()
            if data["result"]:
                return {
                    "name": data["result"][0]["songname"],
                    "artist": data["result"][0]["artist"],
                    "url": data["result"][0]["url"],
                }
        except Exception as e:
            print(f"Error searching song: {e}")
        return None