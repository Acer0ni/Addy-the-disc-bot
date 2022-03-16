import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
W2G_TOKEN = os.getenv("W2G_TOKEN")


class W2G_helper:
    async def W2G_request(url, **kwargs):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if kwargs.get("headers"):
            kwargs.get("headers").update(headers)
        return requests.post(url, **kwargs)

    async def W2G_create_room(video_url):
        url = "https://w2g.tv/rooms/create.json"
        payload = {
            "w2g_api_key": W2G_TOKEN,
            "share": video_url,
            "bg_color": "#00ff00",
            "bg_opacity": "50",
        }
        response = await W2G_helper.W2G_request(url, json=payload)
        if response.status_code == 200:
            content = json.loads(response.content)
            return content["streamkey"]
        else:
            return none

    async def W2G_play(author, video_url) -> int:
        url = "https://w2g.tv/rooms/{author}/sync_update"
        payload = {"w2g_api_key": W2G_TOKEN, "item_url": url}
        response = await W2G_helper.W2G_request(url, json=payload)
        return response.status_code
