import get_recommendations
import sqlite3

def mehodenathalie1():
    return "dit is methode1"

def party():
    recommendations = get_recommendations.get_genres_for_recommendation(limit=1, seed_genres='pop')
    connection=sqlite3.connect(":memory:")
    with open("createtables.sql") as f:
        query = f.read()
    cursor = connection.cursor()
    cursor.executescript(query)
    print(get_recommendations.get_genres_for_recommendation())