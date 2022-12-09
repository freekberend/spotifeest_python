import sqlite3

import get_recommendations


def mehodenathalie1():
    return "dit is methode1"


def party():
    recommendations = get_recommendations.get_genres_for_recommendation(limit=1, seed_genres='pop')
    connection = sqlite3.connect(":memory:")
    with open("createtables.sql") as f:
        query = f.read()
    cursor = connection.cursor()
    cursor.executescript(query)
    # print(recommendations["tracks"][0]["id"])
    # print(recommendations["tracks"][0]["name"])
    trackid = recommendations["tracks"][0]["id"]
    trackname = recommendations["tracks"][0]["name"]
    cursor.execute("insert into track values (?,?)", (trackid, trackname))

    for artist in recommendations["tracks"][0]["artists"]:
        # print(artist["genres"])
        # print(artist["name"])
        # print(artist["id"])
        artist_id = artist["id"]
        artist_name = artist["name"]
        cursor.execute("INSERT INTO artist VALUES (?, ?, ?)", (artist_id, artist_name, trackid))

        connection.commit()
        genres_in_database = cursor.execute("SELECT genre FROM genre;").fetchall()
        # print(genres_in_database)
        genres = artist["genres"]
        for genre in genres:
            if genre not in genres_in_database:
                cursor.execute("INSERT INTO genre (genre, artist_id) VALUES (?, ?)", (genre, artist_id))

    connection.commit()
    with open("joined_select.sql") as f:
        query = f.read()
    data = cursor.execute(query).fetchall()
    kolommen = [i[0] for i in cursor.description]
    data_str = ""
    data_lijst = []
    for regel in data:
        new = {}
        for key, value in zip(kolommen, regel):
            # print(key, value, sep=': ', end='')
            data_str += f"{key}: {value}, "
            new[key] = value
        data_str = data_str[:-2] + '<br>'
        data_lijst.append(new)
    return data_lijst
