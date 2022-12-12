import json
import sqlite3

import get_recommendations


def mehodenathalie1():
    return "dit is methode1"


def party():
    connection = sqlite3.connect(":memory:")
    vul_database(connection)

    cursor = connection.cursor()
    # lees database
    with open("joined_select.sql") as f:
        query = f.read()
    data = cursor.execute(query).fetchall()
    kolommen = [i[0] for i in cursor.description]
    data_str = ""
    data_lijst = []
    for regel in data:
        new = {}
        for key, value in zip(kolommen, regel):
            data_str += f"{key}: {value}, "
            new[key] = value
        data_str = data_str[:-2] + '<br>'
        data_lijst.append(new)
    print(data_lijst)
    return json.dumps(data_lijst, indent=4)


def vul_database(connection, query, cursor):
    with open("createtables.sql") as f:
        query = f.read()
    cursor = connection.cursor()
    cursor.executescript(query)
    te_laden = [
        {
            'type': 'genre',
            'waarde': 'pop',
            'persoon': 'Henk'
        },
        {
            'type': 'genre',
            'waarde': 'pop',
            'persoon': 'Jan'
        },
        {
            'type': 'genre',
            'waarde': 'hip-hop',
            'persoon': 'Harry'
        },
        {
            'type': 'genre',
            'waarde': 'metal',
            'persoon': 'Mara'
        },
        {
            'type': 'genre',
            'waarde': 'punk',
            'persoon': 'Jannie'
        },
    ]
    for item in te_laden * 3:
        if item['type'] == 'genre':
            recommendations = get_recommendations.get_genres_for_recommendation(limit=1, seed_genres=item['waarde'])
        elif item['type'] == 'artist':
            recommendations = get_recommendations.get_genres_for_recommendation(limit=1, seed_artists=item['waarde'])
        elif item['type'] == 'track':
            recommendations = get_recommendations.get_genres_for_recommendation(limit=1, seed_tracks=item['waarde'])
        else:
            raise ValueError('No valid type')

        trackid = recommendations["tracks"][0]["id"]
        trackname = recommendations["tracks"][0]["name"]
        cursor.execute("insert into track values (?, ?, ?)", (trackid, trackname, item['persoon']))

        for artist in recommendations["tracks"][0]["artists"]:
            artist_id = artist["id"]
            artist_name = artist["name"]
            cursor.execute("INSERT INTO artist VALUES (?, ?, ?)", (artist_id, artist_name, trackid))

            connection.commit()
            genres_in_database = cursor.execute("SELECT genre FROM genre;").fetchall()
            genres = artist["genres"]
            for genre in genres:
                if genre not in genres_in_database:
                    cursor.execute("INSERT INTO genre (genre, artist_id) VALUES (?, ?)", (genre, artist_id))
    connection.commit()
