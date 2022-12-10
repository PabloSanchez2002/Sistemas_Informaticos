import collections
import json
import os
import sys
import traceback
import database
import pymongo

from sqlalchemy import create_engine

db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)

def getSQLdata():
    try:
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("SELECT regexp_replace(movietitle, '\(\d\d\d\d\)','') as title,  array_agg(DISTINCT genre) as generes, year, ratingcount as number_of_votes, ratingmean as average_rating, array_agg(DISTINCT directorname) as directors, array_agg(DISTINCT actorname) as actors \
                                    from imdb_movies \
                                    join imdb_moviecountries on imdb_movies.movieid = imdb_moviecountries.movieid \
                                    join imdb_moviegenres on imdb_moviegenres.movieid = imdb_movies.movieid \
                                    join imdb_directormovies on imdb_directormovies.movieid = imdb_movies.movieid \
                                    join imdb_directors on imdb_directormovies.directorid = imdb_directors.directorid \
                                    join imdb_actormovies on imdb_actormovies.movieid = imdb_movies.movieid \
                                    join imdb_actors on imdb_actormovies.actorid = imdb_actors.actorid  \
                                    where imdb_moviecountries.country = 'UK' \
                                    GROUP BY imdb_movies.movieid \
                                    order by year desc \
                                    limit 400;")

        # Convert query to objects of key-value pairs
        objects_list = []
        for film in db_result:
            d = collections.OrderedDict()
            d["title"] = film[0]
            d["genres"] = film[1]
            d["year"] = int(film[2])
            d["number_of_votes"] = film[3]
            d["average_rating"] = film[4]
            d["directors"] = film[5]
            d["actors"] = film[6]
            objects_list.append(d)
        j = json.dumps(objects_list)
        with open("films.json", "w") as f:
            f.write(j)
        print("json creado")
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'



def createMongoDBFromPostgreSQLDB():
    myclient = pymongo.MongoClient('localhost', 27017)
    getSQLdata()
    # Borrar la base de datos si ya existe
    if 'si1' in myclient.list_database_names():
        print("si1 ya existente, actualizamos")
        myclient.drop_database('si1')

    mydb = myclient.si1
    ukCol = mydb.topUK
    with open("films.json", "r") as file:
        file_data = json.load(file)
        os.remove("films.json")
        print("json eliminado")
    
    ukCol.insert_many(file_data)
    #print(myclient.list_database_names())
    database.mongoDBCloseConnect(myclient)


if __name__ == "__main__":
    createMongoDBFromPostgreSQLDB()
