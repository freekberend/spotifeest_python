SELECT *
  FROM track AS t
  JOIN artist AS a
    ON t.track_id = a.track_id
  JOIN genre AS g
    ON a.artist_id = g.artist_id