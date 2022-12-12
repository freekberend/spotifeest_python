import json

import felix
import freek
import get_recommendations
import maarten
import nathalie
import Olaf
import richard
import skott
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/get_recommendations', methods=["POST"])
def get_spotify_recommendations():
    input_json = request.get_json(force=True)
    access_token = get_recommendations.get_access_token()
    recommendations = get_recommendations.get_recommendations_on_spotify(access_token, **input_json)
    return recommendations

@app.route('/get_track_recommendations', methods=["POST"])
def get_track_recommendations():
    input2_json = request.get_json(force=True)
    access_token = get_recommendations.get_access_token()
    track = input2_json["track1"]
    TrackId = get_recommendations.get_id_from_track(access_token, track)
    recommendations = get_recommendations.get_recommendations_on_spotify(access_token, limit=1, seed_tracks= TrackId)
    return recommendations


@app.route('/get_artist_recommendations', methods=["POST"])
def get_artist_recommendations():
    input_json = request.get_json(force=True)
    access_token = get_recommendations.get_access_token()
    artist = input_json["artist1"]
    ArtistId = get_recommendations.get_id_from_artist(access_token, artist)
    recommendations = get_recommendations.get_recommendations_on_spotify(access_token, limit=1, seed_artists= ArtistId)
    return recommendations




@app.route("/felix")
def routefelix():
    return felix.methodefelix1()

@app.route("/olaf")
def routeolaf():
    return Olaf.methodeOlaf()

@app.route("/nathalie")
def routenathalie():
    return nathalie.mehodenathalie1()

@app.route("/nathalieParty")
def routenathalieParty():
    return nathalie.party()

@app.route("/richard")
def routerichard():
    return richard.methoderichard1()

@app.route("/freek")
def routefreek():
    return freek.methodefreek()

@app.route("/maarten")
def routemaarten():
    return maarten.methodemaarten()

@app.route("/skott")
def routeskott():
    return skott.methodeSkott()


@app.route("/docentfreek")
def routedocentfreek():
    return get_recommendations.get_genres_for_recommendation(limit=1, market="NL", seed_genres="pop")


@app.route("/get_track_features/<track_id>")
def route_get_track_features(track_id):
    return get_recommendations.get_track_features(track_id)
