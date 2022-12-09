import get_recommendations

def mehodenathalie1():
    return "dit is methode1"

def party():
    access_token = get_recommendations.get_access_token()
    recommendations = get_recommendations.get_recommendations_on_spotify(access_token, limit=1, seed_genres='pop')
    for artist in recommendations.get("tracks")[0].get("artists"):
        print(artist['id'])
    return recommendations.get("tracks")[0].get("artists")
    return recommendations
