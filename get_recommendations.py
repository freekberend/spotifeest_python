import json

import geheim
import requests

# Client ID en Secret kun je verkrijgen door een app aan te maken in de Spotify developer site (dashboard).

# De te gebruiken API's van Spotify
CLIENT_ID = geheim.CLIENT_ID
CLIENT_SECRET = geheim.CLIENT_SECRET
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_GET_RECOMMENDATIONS_URL = 'https://api.spotify.com/v1/recommendations'
SPOTIFY_SEARCH_ITEM = "https://api.spotify.com/v1/search"
AVAILABLE_GENRE_SEEDS = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
SPOTIFY_ARTIST_BY_ID = "https://api.spotify.com/v1/artists/"


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

#test dataset nathalie
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

#    print(get_id_from_artist(access_token, "The Strokes"))
    TrackId = get_id_from_track(access_token, "Last Nite")
    recoms = get_recommendations_on_spotify(access_token, limit=1, seed_tracks= TrackId)
    print(recoms["tracks"][0]["artists"][0]["name"] + " - " + recoms["tracks"][0]["name"])
    #track_or_artist = input_track_or_artist()
    #print(track_or_artist)
    # voorbeeld van volledige json
    #print(genre)
    
    
#    print(f'{genre["artists"]["items"][0]["genres"]}')

    #print(playlist)
    # print de recommendation (artist - nummer)
    #print(f'{playlist["tracks"][0]["artists"][0]["name"]} - {playlist["tracks"][0]["name"]}')

#    artist, type_, artist_id, track_id = input_track_or_artist(access_token)
#    genre_pref = get_genres_from_input(artist, type_, access_token)
#    print(", ".join(genre_pref[:]))
    
    available_genre_seed_list = get_available_genre_seeds(access_token)["genres"]
    
    genre_pref = ["pop", "soul"]
    for genre in genre_pref:
        if genre in available_genre_seed_list:
            print(genre)
        

#    genre_based_playlist = get_recommendations_on_spotify(
#        access_token = access_token,
#        limit= 1,
#        seed_genres= genre_pref
#    )

#    artist_based_playlist = get_recommendations_on_spotify(
#        access_token = access_token,
#        limit= 10,
#        seed_artists= artist_id
#    )    
    
    print("\n")
    #print(genre_based_playlist)
    #print(f'{genre_based_playlist["tracks"][0]["artists"][0]["name"]} - {genre_based_playlist["tracks"][0]["name"]}')

#    print(f'{artist_based_playlist["tracks"][0]["artists"][0]["name"]} - {artist_based_playlist["tracks"][0]["name"]}')



    #print(get_available_genre_seeds(access_token)["genres"])



    #print(genre["tracks"]["items"][0]["artists"][0]["name"])
    #print(genre["tracks"]["items"])

if __name__ == '__main__':
    main()
