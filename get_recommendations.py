# import json
import os
# import geheim
import requests
# import mysql.connector

# Client ID en Secret kun je verkrijgen door een app aan te maken in de Spotify developer site (dashboard).

# De te gebruiken API's van Spotify
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_GET_RECOMMENDATIONS_URL = 'https://api.spotify.com/v1/recommendations'
SPOTIFY_SEARCH_ITEM = "https://api.spotify.com/v1/search"
AVAILABLE_GENRE_SEEDS = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
SPOTIFY_ARTIST_BY_ID = "https://api.spotify.com/v1/artists/"



# mydb = mysql.connector.connect(user="spotifeest_mysql", password="abcd1234ABCD!@#$", host="yc2211mysql.mysql.database.azure.com", port=3306, database="configuration", ssl_ca="https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem", ssl_disabled=False)

# mycursor = mydb.cursor()
# mycursor.execute("SELECT CLIENT_ID FROM sleutels WHERE ")
# myresult = mycursor.fetchall()
# print(myresult)

def get_access_token():
    auth_response = requests.post(SPOTIFY_AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    })
    return auth_response.json()['access_token']


def get_recommendations_on_spotify(access_token, **kwargs):
    response = requests.get(
        SPOTIFY_GET_RECOMMENDATIONS_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params=kwargs
    )
    return response.json()

def get_available_genre_seeds(access_token, **kwargs):
    response = requests.get(
        AVAILABLE_GENRE_SEEDS,
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params=kwargs
    )
    return response.json()

def get_genre_from_artist_or_songname(access_token, **kwargs):
    # https://developer.spotify.com/console/get-search-item/
    response = requests.get(
        SPOTIFY_SEARCH_ITEM,
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params=kwargs
    )
    return response.json()


def input_track_or_artist(access_token):
    
    print("Pick an artist or track:")
    artist_or_song = input()
    print("Is this an artist or a track?")
    type_ = input()
    jsonresponse = get_genre_from_artist_or_songname(
    access_token = access_token,
    q = artist_or_song,
    type = type_,
    limit= 1,
    )
    artist_id = ""
    track_id = ""
    if type_ == "artist":
        artist = artist_or_song
        artist_id = jsonresponse["artists"]["items"][0]["id"]
        print(jsonresponse["artists"]["items"][0]["id"])
    
    if type_ == "track":
        artist = jsonresponse["tracks"]["items"][0]["artists"][0]["name"]
        type_ = "artist"
        track_id = jsonresponse["tracks"]["items"][0]["id"]
        print(jsonresponse["tracks"]["items"][0]["id"])


    return artist, type_, artist_id, track_id

def get_id_from_artist(access_token, artist):
    type_ = "artist"
    jsonresponse = get_genre_from_artist_or_songname(
    access_token = access_token,
    q = artist,
    type = type_,
    limit= 1,
    )
    return jsonresponse["artists"]["items"][0]["id"]

def get_id_from_track(access_token, track):
    type_ = "track"
    jsonresponse = get_genre_from_artist_or_songname(
    access_token = access_token,
    q = track,
    type = type_,
    limit= 1,
    )
    return jsonresponse["tracks"]["items"][0]["id"]



def get_genres_from_input(artist, type_, access_token):
    jsonresponse = get_genre_from_artist_or_songname(
    access_token = access_token,
    q = artist,
    type = type_,
    limit= 1,
    )
    return jsonresponse["artists"]["items"][0]["genres"]

def get_genres_for_recommendation(**kwargs):
    access_token = get_access_token()
    recommendation = get_recommendations_on_spotify(access_token, **kwargs)
    if not recommendation.get('tracks'):
        raise ValueError(f"Geen tracks voor {kwargs}")
    for index, artist in enumerate(recommendation["tracks"][0]["artists"]):
        artist_info = requests.get(
            SPOTIFY_ARTIST_BY_ID + artist["id"],
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()
        recommendation["tracks"][0]["artists"][index]["genres"] = artist_info["genres"]

    return recommendation


def get_track_features(track_ids):
    if not isinstance(track_ids, list):
        return requests.get(f"https://api.spotify.com/v1/audio-features/{track_ids}",
                            headers={"Authorization": f"Bearer {get_access_token()}"}
                            ).json()

    track_data = []
    for one_track_id in track_ids:
        track_features = requests.get(f"https://api.spotify.com/v1/audio-features/{one_track_id}",
                                      headers={"Authorization": f"Bearer {get_access_token()}"}
                                      ).json()
        track_data.append(track_features)

    return track_data

def createPlaylist(access_token):
    user_id = "1133249149"
    endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    request_body = json.dumps({
            "name": "Indie bands like Franz Ferdinand but using Python",
            "description": "My first programmatic playlist, yooo!",
            "public": False # let's keep it between us - for now
            })
    response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                            "Authorization":access_token})

def main():
    # Haal een nieuwe access token op 
    access_token = get_access_token()

    playlist = get_recommendations_on_spotify(
        access_token = access_token,
        market= "NL",
        limit= 1,
        seed_genres="metal, classical, pop, trash metal, funk"
    )

    genre = get_genre_from_artist_or_songname(
        access_token = access_token,
        q = "Reptilia",
        type = "track",
        limit= 1,
    )

    TrackId = get_id_from_track(access_token, "Last Nite")
    recoms = get_recommendations_on_spotify(access_token, limit=1, seed_tracks= TrackId)
    print(recoms["tracks"][0]["artists"][0]["name"] + " - " + recoms["tracks"][0]["name"])

    

    available_genre_seed_list = get_available_genre_seeds(access_token)["genres"]
    
    genre_pref = ["pop", "soul"]
    for genre in genre_pref:
        if genre in available_genre_seed_list:
            print(genre)
    
    print(createPlaylist(access_token))
        


if __name__ == '__main__':
    main()
