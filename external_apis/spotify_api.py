import requests


class SpotifyTierI:
    def __init__(self, client_id, client_secret):
        data = f"grant_type=client_credentials&client_id={client_id}" \
               f"&client_secret={client_secret}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        result = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
        access_token = result.json()['access_token']
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get_artist_by_id(self, artist_id: str):
        result = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}",
                              headers=self.headers).json()
        return result

