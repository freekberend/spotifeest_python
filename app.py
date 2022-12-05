from flask import Flask
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


@app.route("/felix")
def routefelix():
    return felix.methodefelix1()

@app.route("/olaf")
def routeolaf():
    return Olaf.methodeOlaf()

@app.route("/nathalie")
def routenathalie():
    return nathalie.methodenathalie1()

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