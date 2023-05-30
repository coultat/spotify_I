import requests
from typing import Optional, Dict, List

import pydantic


class Followers(pydantic.BaseModel):
    href: Optional[str]
    total: int


class Images(pydantic.BaseModel):
    height: int
    url: str
    width: int


class Artist(pydantic.BaseModel):
    external_urls: Dict[str, str]
    followers: Followers
    genres: List[str]
    href: str
    id: str
    images: List[Images]
    name: str
    popularity: int
    type: str
    uri: str

class Spotify():
    def __init__(self, client_id: str, client_secret: str):
        data = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        result = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
        access_token = result.json()['access_token']
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get_artist_by_id(self, artist_id: str):
        result = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}",
                              headers=self.headers)
        return result


