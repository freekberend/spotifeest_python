import requests
import json

# Client ID en Secret kun je verkrijgen door een app aan te maken in de Spotify developer site (dashboard).

# De te gebruiken API's van Spotify
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_GET_RECOMMENDATIONS_URL = 'https://api.spotify.com/v1/recommendations'
SPOTIFY_SEARCH_ITEM = "https://api.spotify.com/v1/search"

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

#def input_track_or_artist():
#    x = input()

#print(x)



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
        q = "Metallica",
        type = "artist",
        limit= 1,
    )
    # voorbeeld van volledige json
    #print(genre)
    
    
    # print(f'{genre["artists"]["items"][0]["genres"]}')

    print(playlist)
    # print de recommendation (artist - nummer)
    print(f'{playlist["tracks"][0]["artists"][0]["name"]} - {playlist["tracks"][0]["name"]}')



if __name__ == '__main__':
    main()
