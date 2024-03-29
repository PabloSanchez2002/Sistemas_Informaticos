CREATE OR REPLACE FUNCTION updateratingsfunc() 
RETURNS TRIGGER as $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        UPDATE imdb_movies SET ratingcount = (select count(customerid) from ratings WHERE movieid = new.movieid) WHERE movieid = new.movieid ;
        UPDATE imdb_movies SET ratingmean = (select avg(rated) from ratings WHERE movieid = new.movieid) WHERE movieid = new.movieid;
    ELSEIF (TG_OP = 'DELETE') THEN    
        UPDATE imdb_movies SET ratingcount = (select count(customerid) from ratings WHERE movieid = old.movieid) WHERE movieid = old.movieid ;
        UPDATE imdb_movies SET ratingmean = (select avg(rated) from ratings WHERE movieid = old.movieid) WHERE movieid = old.movieid;
    ELSEIF (TG_OP = 'UPDATE') THEN
        UPDATE imdb_movies SET ratingmean = (select avg(rated) from ratings WHERE movieid = new.movieid) WHERE movieid = new.movieid;
    END IF;
    RETURN NULL; 
END;
$$ 
LANGUAGE 'plpgsql';

--Trigger para cuando se mete o elimina una valoracion
CREATE OR REPLACE TRIGGER updateratings
AFTER DELETE OR INSERT OR UPDATE ON ratings
FOR EACH ROW
EXECUTE PROCEDURE updateratingsfunc();



