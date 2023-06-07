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
    followers: Optional[Followers]
    genres: List[str]
    href: str
    spotify_artist_id: str = Field(alias="id")
    images: List[Images]
    name: str
    popularity: int
    artist_type: str = Field(alias='type')
    uri: str
    class Config:
        allow_population_by_field_name = True
