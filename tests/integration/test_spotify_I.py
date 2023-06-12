import json

import pytest

from models.models import Artist
from spotify_I.Spotify_I import create_app

@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()
    yield client


def test_populate_db_10_artists(client):
    # Given the instance of the API

    # And a list with spotify artist ids
    spotify_artists_ids = [
        "7dlqUnjoF2U2DkNDMhcgG4",  # Hilltop Hoods
        "2d9LRvQJnAXRijqIJDDs2K",  # Emicida
        "4Va55p3P2P96lIgzntievo",  # Nação Zumbi
        "2d0hyoQ5ynDBnkvAbJKORj",  # RATM
        "6FQqZYVfTNQ1pCqfkwVFEa",  # Foals
        "356c8AN5YWKvz86B4Sb1yf",  # Rival Sons
        "6Mo9PoU6svvhgEum7wh2Nd",  # Public Enemy
        "0cmWgDlu9CwTgxPhf403hb",  # Bonobo
        "03r4iKL2g2442PT9n2UKsx",  # Beastie Boys
        "30uiS1n3uIGXJEYFR1GVDy",  # The Brian Jonestown Massacre
        "3iOvXCl6edW5Um0fXEBRXy",  # The XX
    ]

    # And the expected_result_message
    expected_result_message = 'Artist inserted in the Data Base'

    # When populating the DB
    for spotify_artist_id in spotify_artists_ids:
        result = client.post(f"/db/artist/{spotify_artist_id}")
        assert result.status_code == 200
        assert result.json['message'] == expected_result_message

    # And the tables are dropped
    del_result = client.delete('/db')
    assert del_result.status_code == 200
    assert del_result.json['message'] == 'tables from the db dropped'

def test_get_artist_spotify_by_id(client):
    # Given the instance of the api

    # And the spotify_artist_id as input
    input_value = "03r4iKL2g2442PT9n2UKsx"

    # And the expected name
    expected_name = 'Beastie Boys'

    # When fetching the artist from spotify through the input value
    result = client.get(f"/spotify/artist/{input_value}")
    artist = Artist.parse_obj(result.json)

    # Then the result must be 200 and match the expected_name
    assert result.status_code == 200
    assert artist.name == expected_name


def test_get_artist_spotify_by_id_bad_request(client):
    # Given the instance of the api

    # And the wrong_spotify_artist_id as input
    input_value = "WRONG_ID"

    # And the expected value
    expected_result = {'error': {'message': 'invalid id', 'status': 400}}

    # When fetching the artist from spotify through the input value
    result = client.get(f"/spotify/artist/{input_value}")

    # Then the result must be 200 and match the expected_name
    assert result.status_code == 200
    assert result.json == expected_result


def test_insert_artist_db(client):
    # Given the instance of the API

    # And the artist_id to be fetched in Spotify API
    input_value_id = '46aNfN89JrOQTCy97GoCHa'

    # And the expected value
    expected_response = 'Artist inserted in the Data Base'

    # When inserting the data in the db
    result = client.post(f"/db/artist/{input_value_id}")

    # Then the result must match the expected value
    assert result.json['message'] == expected_response

    # And the tables are dropped
    del_result = client.delete('/db')
    assert del_result.status_code == 200
    assert del_result.json['message'] == 'tables from the db dropped'


def test_insert_repeated_artist_db(client):
    # Given the instance of the API

    # And inserting the artist in the db
    input_value_id = '46aNfN89JrOQTCy97GoCHa'
    result = client.post(f"/db/artist/{input_value_id}")
    assert result.status_code == 200

    # And the expected error message
    expected_result = f'The artist with the id {input_value_id} was already in the db'

    # When inserting the same artist again in the db
    result = client.post(f"/db/artist/{input_value_id}")

    # Then the result matches the expected_result
    result.json['message'] == expected_result

    # And the tables are dropped
    del_result = client.delete('/db')
    assert del_result.status_code == 200
    assert del_result.json['message'] == 'tables from the db dropped'


def test_update_name_artist_by_spotify_artist_id(client):
    # Given the instance of the API

    # And the new_name as input value
    input_new_name = 'The Heavy'

    # And inserting the artist in the db
    input_value_id = '46aNfN89JrOQTCy97GoCHa'
    result = client.post(f"/db/artist/{input_value_id}")
    assert result.status_code == 200

    # And the expected result message
    expected_message = f'artist name sucessfully changed to {input_new_name}'

    # When updating the name of the artist by spotify_artist_id
    result = client.patch("/artist",
                        json={'spotify_artist_id': input_value_id,
                              'new_name': input_new_name})

    # Then the result message must match the expected result message
    assert result.status_code == 200
    assert result.json['message'] == expected_message

    # And the tables are dropped
    del_result = client.delete('/db')
    assert del_result.status_code == 200
    assert del_result.json['message'] == 'tables from the db dropped'


def test_wrong_update_name_artist_by_spotify_artist_id(client):
    # Given the instance of the API

    # And the new_name as input value
    input_new_name = 'The Heavy'

    # And inserting the artist in the db
    input_value_id = '46aNfN89JrOQTCy97GoCHa'
    result = client.post(f"/db/artist/{input_value_id}")
    assert result.status_code == 200

    # And the expected result message
    expected_message = f'There was no artists found with the spotyf_artist_id {input_value_id}a in the DB'

    # When updating the name of the artist by spotify_artist_id
    result = client.patch("/artist",
                          json={'spotify_artist_id': input_value_id + 'a',
                                'new_name': input_new_name})

    # Then the result message must match the expected result message
    assert result.status_code == 200
    assert result.json['message'] == expected_message

    # And the tables are dropped
    del_result = client.delete('/db')
    assert del_result.status_code == 200
    assert del_result.json['message'] == 'tables from the db dropped'


def test_update_artist(client):
    # Given the instance of the API

    # And the spotify_artist_id for the input value
    input_value_1 = '3nDNDLcZuSto4k9u4AbcLB'  # Marteria
    input_value_2 = '2ye2Wgw4gimLv2eAKyk1NB'  # Metallica

    # And the expected_message_result
    expected_message_result = "Artist successfully updated"

    # And introducing the data of the first artist in the DB
    result = client.post(f"/db/artist/{input_value_1}")

    # And getting the artist pydantic model
    artist = Artist.parse_obj(client.get(f"/spotify/artist/{input_value_2}").json)

    # And adding the spotify_artist_id from the original to the dict
    artist = artist.dict()
    artist['previous_artist'] = input_value_1

    # When updating with a put
    result = client.put(f"/artist/{input_value_1}",
                        json=artist)

    # Then the result must be satisfactory
    assert result.status_code == 200
    assert result.json['message'] == expected_message_result

    # And the tables are dropped
    del_result = client.delete('/db')
    assert del_result.status_code == 200
    assert del_result.json['message'] == 'tables from the db dropped'


def test_delete_artist(client):
    # Given the instance of the API

    # And inserting the artist in the db
    input_value_id = '46aNfN89JrOQTCy97GoCHa'
    result = client.post(f"/db/artist/{input_value_id}")
    assert result.status_code == 200
    assert result.json['message'] == 'Artist inserted in the Data Base'

    # And the expected_result_message
    expected_result_message = 'Artist name successfully deleted'

    # When deleting the artist
    result = client.delete(f"/artist/{input_value_id}")

    # Then the result must be good
    assert result.json['message'] == expected_result_message
    assert result.status_code == 200

    # And the tables are dropped
    del_result = client.delete('/db')
    assert del_result.status_code == 200
    assert del_result.json['message'] == 'tables from the db dropped'
