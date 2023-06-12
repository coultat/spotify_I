from typing import Generator, Dict

import sqlite3
from contextlib import closing

from spotify_I.models.models import Artist


class SpotifySqlite3:
    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS artists "
                            "(id INTEGER PRIMARY KEY AUTOINCREMENT, genres VARCHAR(255), href TEXT, "
                            "spotify_artist_id TEXT UNIQUE, name TEXT NOT NULL, popularity INTEGER, artist_type TEXT, uri TEXT)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS images " 
                            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "spotify_artist_id TEXT, "
                            "height INTEGER,"
                            "url TEXT,"
                            "width INTEGER, "
                            "FOREIGN KEY(spotify_artist_id) REFERENCES artists(spotify_artist_id))")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS followers " 
                            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "spotify_artist_id TEXT, "
                            "href TEXT,"
                            "total INTEGER,"
                            "FOREIGN KEY(spotify_artist_id) REFERENCES artists(spotify_artist_id))")


    def delete_tables(self):
        self.cursor.execute("DROP TABLE artists")
        self.cursor.execute("DROP TABLE images")
        self.cursor.execute("DROP TABLE followers")

    def get_artist_by_id(self, artist_id: str) -> Artist:
        query = """
                SELECT *
                FROM artists
                WHERE spotify_artist_id = (?)
                """
        args_insert = (artist_id, )
        self.cursor.execute(query, args_insert)
        result = self.cursor.fetchall()
        return result

    def insert_artist_to_db(self, artist: Artist):
        query = """
                INSERT INTO artists
                (genres, href, spotify_artist_id, name, popularity, artist_type, uri)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
        args_input = (str(artist.genres),
                      artist.href,
                      artist.spotify_artist_id,
                      artist.name,
                      artist.popularity,
                      artist.artist_type,
                      artist.uri)
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, args_input)
            self.connection.commit()
            last_id = cursor.lastrowid
        return last_id

    def insert_images_to_db(self, artist: Artist):
        query = """
                INSERT INTO images
                (spotify_artist_id, height, url, width)
                VALUES (?, ?, ?, ?)
                """
        with closing(self.connection.cursor()) as cursor:
            for image in artist.images:
                args_input = (artist.spotify_artist_id, image.height, image.url, image.width)
                cursor.execute(query, args_input)
                self.connection.commit()

    def insert_followers_into_db(self, artist: Artist):
        query = """
                INSERT INTO followers
                (spotify_artist_id, href, total)
                VALUES(?, ?, ?)
                """

        with closing(self.connection.cursor()) as cursor:
            args_input = (artist.spotify_artist_id, artist.followers.href, artist.followers.total)
            cursor.execute(query, args_input)
            self.connection.commit()

    def update_artist_name(self, new_name: str, spotify_artist_id: str) -> Dict[str, str]:
        query = """
                UPDATE artists
                SET name = ?
                WHERE spotify_artist_id = ?
                """
        args_insert = (new_name, spotify_artist_id, )
        self.cursor.execute(query, args_insert )
        self.connection.commit()
        return {'message': f'artist name sucessfully changed to {new_name}'}

    def update_artist(self, artist: Artist, spotify_artist_id: str) -> Dict[str, str]:
        query = """
                UPDATE artists
                SET genres = ?, 
                href = ?, 
                spotify_artist_id = ?, 
                name = ?, 
                popularity = ?, 
                artist_type = ?, 
                uri = ?
                WHERE spotify_artist_id = ?
                """
        args_input = (str(artist.genres),
                      artist.href,
                      artist.spotify_artist_id,
                      artist.name,
                      artist.popularity,
                      artist.artist_type,
                      artist.uri,
                      spotify_artist_id)
        self.cursor.execute(query, args_input )
        self.connection.commit()
        self.connection.close()
        return {'message': f'Artist successfully updated'}

    def delete_artist_by_spotify_id(self, spotify_artist_id: str) -> Dict[str, str]:
        query = """
                DELETE FROM artists
                WHERE spotify_artist_id = ?
                """
        args_input = (spotify_artist_id, )
        self.cursor.execute(query, args_input)
        self.connection.commit()
        self.connection.close()
        return {'message': f'Artist name successfully deleted'}
