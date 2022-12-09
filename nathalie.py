import sqlite3

import get_recommendations


def mehodenathalie1():
    return "dit is methode1"


def party():
    connection = sqlite3.connect(":memory:")
    with open("createtables.sql") as f:
        query = f.read()
    cursor = connection.cursor()
    cursor.executescript(query)
    # print(recommendations["tracks"][0]["id"])
    # print(recommendations["tracks"][0]["name"])
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

        # {
        #     'type': 'artist',
        #     'waarde': 'Justin Timberlake',
        #     'persoon': 'Henk'
        # },
        # {
        #     'type': 'artist',
        #     'waarde': 'Lady Gaga',
        #     'persoon': 'Jan'
        # },
        # {
        #     'type': 'artist',
        #     'waarde': 'AURORA',
        #     'persoon': 'Harry'
        # },
        # {
        #     'type': 'artist',
        #     'waarde': 'Eminem',
        #     'persoon': 'Mara'
        # },
        # {
        #     'type': 'artist',
        #     'waarde': 'Dream Theater',
        #     'persoon': 'Jannie'
        # },

        # {
        #     'type': 'track',
        #     'waarde': 'Expiration Date',
        #     'persoon': 'Henk'
        # },
        # {
        #     'type': 'track',
        #     'waarde': 'Sound of Silence',
        #     'persoon': 'Jan'
        # },
        # {
        #     'type': 'track',
        #     'waarde': 'Hot Mess',
        #     'persoon': 'Harry'
        # },
        # {
        #     'type': 'track',
        #     'waarde': 'Beggin\'',
        #     'persoon': 'Mara'
        # },
        # {
        #     'type': 'track',
        #     'waarde': 'SUPERMODEL',
        #     'persoon': 'Jannie'
        # }
    ]
    for item in te_laden:
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
    for regel in data:
        for key, value in zip(kolommen, regel):
            print(key, value, sep=': ', end='')
            data_str += f"{key}: {value}, "
        data_str = data_str[:-2] + '<br>'
    return data_str
