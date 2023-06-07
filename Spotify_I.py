from typing import Dict

from flask import Flask, request

from models.models import Artist
from external_apis.spotify_api import SpotifyTierI
from db.sqlite3 import SpotifySqlite3

# Todo -> type hint
DB_NAME = '../../tier1.db'

def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    @app.route("/artist/<spotify_artist_id>", methods=['GET'])
    def get_artist_by_id(spotify_artist_id: str) -> Artist:
        result = SpotifySqlite3(DB_NAME).get_artist_by_id(spotify_artist_id)
        return Artist.parse_obj(result)

    @app.route("/spotify/artist/<spotify_artist_id>", methods=['GET'])
    def get_artist_spotify_by_id(spotify_artist_id: str) -> Artist:
        return SpotifyTierI(client_id='e71369f30b614d7b90d2164bc279397d', client_secret='eef48fe4d2e74ca8809f0c218beae7e0').get_artist_by_id(spotify_artist_id)  # Todo change how to send the client_od and client_secret

    @app.route("/db/artist/<spotify_artist_id>", methods=['POST'])
    def insert_artist_into_db_by_spotify_id(spotify_artist_id: str) -> Dict[str, str]:
        artist_db = SpotifySqlite3(DB_NAME).get_artist_by_id(spotify_artist_id)
        if artist_db:
            return {'message': f'The artist with the id {spotify_artist_id} was already in the db'}
        result = SpotifyTierI(client_id='e71369f30b614d7b90d2164bc279397d',
                              client_secret='eef48fe4d2e74ca8809f0c218beae7e0').get_artist_by_id(spotify_artist_id) # Todo change credentials to somewhere else
        artist = Artist.parse_obj(result)
        result = SpotifySqlite3(DB_NAME).insert_artist_to_db(artist)
        SpotifySqlite3(DB_NAME).insert_images_to_db(artist)
        return {'message': 'Artist inserted in the Data Base', 'artist_id': result}

    @app.route('/db', methods=['DELETE'])
    def drop_tables_from_db() -> Dict[str, str]:
        SpotifySqlite3(DB_NAME).delete_tables()
        return {'message': 'tables from the db dropped'}

    @app.route("/artist", methods=['PATCH'])
    def update_name_artist_by_spotify_artist_id() -> Dict[str, str]:
        spotify_artist_id = request.json['spotify_artist_id']
        new_name = request.json['new_name']
        result = SpotifySqlite3(DB_NAME).get_artist_by_id(spotify_artist_id)
        if result:
            return SpotifySqlite3(DB_NAME).update_artist_name(new_name, spotify_artist_id)
        return {'message': f'There was no artists found with the spotyf_artist_id {spotify_artist_id} in the DB'}


    @app.route("/artist/<spotify_artist_id>", methods=['PUT'])
    def update_artist(spotify_artist_id: str) -> Dict[str, str]:
        artist = Artist.parse_obj(request.get_json())
        result = SpotifySqlite3(DB_NAME).get_artist_by_id(spotify_artist_id)
        if result:
            return SpotifySqlite3(DB_NAME).update_artist(artist, spotify_artist_id)
        return {"message": f"There are no artists with the spotify artist id: {spotify_artist_id}"}

    @app.route("/artist/<spotify_artist_id>", methods=['DELETE'])
    def delete_artist_by_spotify_id(spotify_artist_id: str) -> Dict[str, str]:
        result = SpotifySqlite3(DB_NAME).get_artist_by_id(spotify_artist_id)
        if result:
            return SpotifySqlite3(DB_NAME).delete_artist_by_spotify_id(spotify_artist_id)
        return {"message": f"There are no artists with the spotify artist id: {spotify_artist_id}"}

    return app
