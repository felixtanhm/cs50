SELECT title, rating
FROM movies
JOIN ratings ON ratings.movie_id = movies.id
WHERE movies.year = 2010 AND rating IS NOT NULL
ORDER BY rating DESC, title ASC;
