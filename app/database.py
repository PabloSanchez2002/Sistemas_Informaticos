# -*- coding: utf-8 -*-

import os
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)
# cargar una tabla
db_table_movies = Table('imdb_movies', db_meta, autoload=True, autoload_with=db_engine)

def db_topMovies(y1, y2, MAX):
    try:# conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        db_result=db_conn.execute(f"select * from gettopsales({y1},{y2})")
        info = list(db_result) 
        if len(info) > 10:
            info = info[0:10]
        if len(info) > int(MAX):
            info = info[0:MAX]
        for i in info:
            db_result=db_conn.execute(f"select movieid from imdb_movies where movietitle = '{i[1]}'")
            print(list(db_result))
        print(i)
        db_conn.close()
        return info 
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def db_actMovie(movieid, userid, rating):
    try:# conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute(f"select * from ratings where customerid={userid} and movieid={movieid}")
        if len(list(db_result)) == 1:
            db_conn.execute(f"update ratings set rated={rating} where customerid={userid} and movieid={movieid}")
        else:
            db_conn.execute(f"insert into ratings(customerid, movieid, rated) values({userid},{movieid},{rating}) ")
        info = list(db_result) 
        db_conn.close()
        return info 
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'



def db_getPassword(username):
    try:# conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("select password, balance, customerid from customers where username='%s'"%username)
        info = list(db_result) 
        db_conn.close()
        return info 
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def db_getPrice(movieid):
    try:# conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("select min(price) from products where movieid = '%s'"%movieid)
        info = list(db_result) 
        db_conn.close()
        return  info 
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def db_getGenres(movieid):
    try:# conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("select cm.genres from imdb_catalogogenres cm join imdb_moviegenres mg on mg.genre = cm.id where mg.movieid = '%s'"%movieid)
        info = list(db_result) 
        db_conn.close()
        return  info 
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def db_getMovie(movieid):
    try:# conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("select im.movietitle, im.movieid, im.ratingmean, sum(stock) from imdb_movies im join products p on im.movieid = p.movieid join inventory i on i.prod_id = p.prod_id where im.movieid = '%s' group by im.movieid"%movieid)
        db_result_acts = db_conn.execute("select a.actorname, am.character from imdb_actors a join imdb_actormovies am on a.actorid = am.actorid where am.movieid = '%s' LIMIT 3"%movieid)
        db_result_directs = db_conn.execute("select d.directorname from imdb_directors d join imdb_directormovies dm on d.directorid = dm.directorid where dm.movieid = '%s' "%movieid)
        info = [list(db_result) ,list(db_result_acts) , list(db_result_directs)]
        db_conn.close()
        return  info 
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_initMovies():
    try:# conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("select * from imdb_movies order by movieid LIMIT 16")
        result = list(db_result)
        db_conn.close()
        return result
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'




def db_listOfMovies1949():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Seleccionar las peliculas del anno 1949
        db_movies_1949 = select([db_table_movies]).where(text("year = '1949'"))
        db_result = db_conn.execute(db_movies_1949)
        #db_result = db_conn.execute("Select * from imdb_movies where year = '1949'")
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
