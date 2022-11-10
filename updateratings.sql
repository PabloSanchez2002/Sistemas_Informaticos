CREATE OR REPLACE FUNCTION updateratingsfuncADD() 
RETURNS TRIGGER as $$
BEGIN
    UPDATE imdb_movies SET ratingcount = (select count(customerid) from ratings WHERE movieid = new.movieid) WHERE movieid = new.movieid ;
    UPDATE imdb_movies SET ratingmean = (select avg(rated) from ratings WHERE movieid = new.movieid) WHERE movieid = new.movieid;
    RETURN NEW; 
END;
$$ 
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION updateratingsfuncDEL() 
RETURNS TRIGGER as $$
BEGIN
    UPDATE imdb_movies SET ratingcount = (select count(customerid) from ratings WHERE movieid = new.movieid) WHERE movieid = old.movieid ;
    UPDATE imdb_movies SET ratingmean = (select avg(rated) from ratings WHERE movieid = new.movieid) WHERE movieid = old.movieid;
    RETURN NEW; 
END;
$$ 
LANGUAGE 'plpgsql';

