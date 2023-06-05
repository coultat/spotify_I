from typing import Optional, Dict, List

from pydantic import BaseModel, Field


class Followers(BaseModel):
    href: Optional[str]
    total: int


class Images(BaseModel):
    height: int
    url: str
    width: int


class Artist(BaseModel):
    external_urls: Dict[str, str]
    followers: Followers
    genres: List[str]
    href: str
    spotify_artist_id: str = Field(alias="id")
    images: List[Images]
    name: str
    popularity: int
    type: str
    uri: str
