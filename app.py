from flask import Flask, request, jsonify
import json
import get_recommendations
import felix
import Olaf
import nathalie
import richard
import freek
import skott
import maarten

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