CREATE TABLE track(
    track_id TEXT PRIMARY KEY NOT NULL,
    track TEXT NOT NULL
);

CREATE TABLE artist(
    artist_id TEXT PRIMARY KEY NOT NULL,
    artist TEXT NOT NULL,
    track_id TEXT NOT NULL,
    FOREIGN KEY (track_id) REFERENCES track (track_id)
);

CREATE TABLE genre(
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre TEXT NOT NULL,
    artist_id TEXT NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artist (artist_id)
);