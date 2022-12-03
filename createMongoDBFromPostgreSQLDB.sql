SELECT imdb_movies.movieid, regexp_replace(movietitle, '\(\d\d\d\d\)','') as movietitle, year, genre, ratingcount, ratingmean, directorname, actorname
    from imdb_movies 
        join imdb_moviecountries on imdb_movies.movieid = imdb_moviecountries.movieid 
        join imdb_moviegenres on imdb_moviegenres.movieid = imdb_movies.movieid
        join imdb_directormovies on imdb_directormovies.movieid = imdb_movies.movieid
        join imdb_directors on imdb_directormovies.directorid = imdb_directors.directorid
        join imdb_actormovies on imdb_actormovies.movieid = imdb_movies.movieid
        join imdb_actors on imdb_actormovies.actorid = imdb_actors.actorid  

    where imdb_moviecountries.country = 'UK'
    order by year desc
    limit 400;
    


SELECT im.movieid, genre
    from imdb_movies im
        join imdb_moviegenres mg on mg.movieid = im.movieid;

    
--https://www.w3schools.com/python/python_mongodb_insert.asp 
