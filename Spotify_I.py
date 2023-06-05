from flask import jsonify, Flask, request

from models.models import Artist
from external_apis.spotify_api import SpotifyTierI
from db.sqlite3 import SpotifySqlite3


DB_NAME = '../../tier1.db'

def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    @app.route("/artist/<spotify_artist_id>", methods=['GET'])
    def get_artist_by_id(spotify_artist_id: str):
        result = SpotifySqlite3(DB_NAME).get_artist_by_id(spotify_artist_id)
        return Artist.parse_obj(result)

    @app.route("/spotify/artist/<spotify_artist_id>", methods=['GET'])
    def get_artist_spotify_by_id(spotify_artist_id: str)-> Artist:
        return SpotifyTierI(client_id='e71369f30b614d7b90d2164bc279397d', client_secret='eef48fe4d2e74ca8809f0c218beae7e0').get_artist_by_id(spotify_artist_id)  # Todo change how to send the client_od and client_secret

    @app.route("/db/artist/<spotify_artist_id>", methods=['POST'])
    def insert_artist_into_db_by_spotify_id(spotify_artist_id: str):
        artist_db = SpotifySqlite3(DB_NAME).get_artist_by_id(spotify_artist_id)
        if artist_db:
            return {'message': f'The artist with the id {spotify_artist_id} was already in the db'}
        result = SpotifyTierI(client_id='e71369f30b614d7b90d2164bc279397d',
                              client_secret='eef48fe4d2e74ca8809f0c218beae7e0').get_artist_by_id(spotify_artist_id)
        artist = Artist.parse_obj(result)
        result = SpotifySqlite3(DB_NAME).insert_artist_to_db(artist)
        SpotifySqlite3(DB_NAME).insert_images_to_db(artist)
        return {'message': 'Artist inserted in the Data Base', 'artist_id': result}

    @app.route('/db', methods=['DELETE'])
    def drop_tables_from_db():
        SpotifySqlite3(DB_NAME).delete_tables()
        return {'message': 'tables from the db dropped'}


    return app
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)



#
#     def save_artist_db(self, artist: Artist) -> None:
#         SpotifySqlite3('tier1.db').insert_artist_to_db(artist)
#
#     def delete_tables(self):
#         SpotifySqlite3('tier1.db').delete_tables()
#
#     def get_artist_from_db_by_id(self, artist_id: str) -> Artist:
#         result = SpotifySqlite3('tier1.db').get_artist_by_id(artist_id)
#         return Artist.parse_obj(result)


# Perguntas para o Marcelo,
# mudar as credentials da API do spotify
# Estructura de helpers, models e errors. Está bem? alguma outra sugerencia?
# Como fazer o criar tables?
# como mandar o nome da db cada vez que conectamos?
# Onde fechar a db?
# Quê porra é essa do Postgresql y como eu posso fazer pra implementar nisto?
