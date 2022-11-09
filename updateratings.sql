CREATE OR REPLACE FUNCTION updateratingsfunc() 
RETURNS TRIGGER as $$
BEGIN
    UPDATE imdb_movies SET ratingcount = (ratingcount + 1) WHERE imdb_movies.movieid = new.movieid;
    UPDATE imdb_movies SET ratingmean = ((ratingmean * (ratingcount - 1) + new.rated)/ratingcount) WHERE movieid = new.movieid;
    RETURN NEW; 
END;
$$ 
LANGUAGE 'plpgsql';
