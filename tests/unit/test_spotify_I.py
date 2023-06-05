import json

import pytest

from models.models import Artist
from spotify_I.Spotify_I import create_app

@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()
    yield client


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
    result.json['message']  == expected_result

    # And the tables are dropped
    del_result = client.delete('/db')
    assert del_result.status_code == 200
    assert del_result.json['message'] == 'tables from the db dropped'


