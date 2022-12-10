COPY ( SELECT row_to_json(result) 
FROM(
 SELECT regexp_replace(movietitle, '\(\d\d\d\d\)','') as title,  array_agg(DISTINCT genre) as generes, year, ratingcount as number_of_votes, ratingmean as average_rating, array_agg(DISTINCT directorname) as directors, array_agg(DISTINCT actorname) as actors
    from imdb_movies 
        join imdb_moviecountries on imdb_movies.movieid = imdb_moviecountries.movieid 
        join imdb_moviegenres on imdb_moviegenres.movieid = imdb_movies.movieid
        join imdb_directormovies on imdb_directormovies.movieid = imdb_movies.movieid
        join imdb_directors on imdb_directormovies.directorid = imdb_directors.directorid
        join imdb_actormovies on imdb_actormovies.movieid = imdb_movies.movieid
        join imdb_actors on imdb_actormovies.actorid = imdb_actors.actorid  

    where imdb_moviecountries.country = 'UK'
    GROUP BY imdb_movies.movieid
    order by year desc
    limit 400
    )as result)
    TO '/tmp/mongoDB.json' WITH (FORMAT text, HEADER FALSE);
    


    
    '''PARA CARGARLO AL DB
    mongoimport --db si1 --collection topUK --file /tmp/mongoDB.json

    cls (clear)
    use si1
    show si1
    show databases
    db.createCollection('topUK')
    .drop()
    .insert()
    .insertMany()
    .update()
    .updateOne()
    .updateMany()
    .find()
     
    '''
    COMANDOS 
    sudo systemctl restart mongod
    systemctl status mongod
    
    psql si1 alumnodb

    entrer shell mongo -> mongo


    sudo service postgresql restart
    sudo service postgresql status


--https://www.w3schools.com/python/python_mongodb_insert.asp 
https://github.com/RubGarFue/SI/blob/60e08cb41d1b0ffb995d60408057b20cb2568677/practica3/app/createMongoDBFromPostgreSQLDB.py
