#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
from app import app
from app import database
from flask import render_template, request, url_for
import os
import sys
import time

@app.route('/', methods=['POST','GET'])
@app.route('/index', methods=['POST','GET'])
def index():
    return render_template('index.html')


@app.route('/borraEstado', methods=['POST','GET'])
def borraEstado():
    if 'state' in request.form:
        state    = request.form["state"]
        bSQL    = request.form["txnSQL"]
        bCommit = "bCommit" in request.form
        bFallo  = "bFallo"  in request.form
        duerme  = request.form["duerme"]
        dbr = database.delState(state, bFallo, bSQL=='1', int(duerme), bCommit)
        return render_template('borraEstado.html', dbr=dbr)
    else:
        return render_template('borraEstado.html')

    
@app.route('/topUK', methods=['POST','GET'])
def topUK():
    # TODO: consultas a MongoDB ...
    colUK = database.getMongoCollection(database.mongo_client)
    
    
    query_a = {"genres": "Comedy", "year": {"$gt": 1990, "$lt": 1992}}
    result_a = colUK.find(query_a)
    movies_a = [mov for mov in result_a]

    query_b = {"$or": [{"year": 1995}, {"year": 1997}, {"year": 1998}], "title": {"$regex": '^.*, The'}, "genres": "Action"}
    result_b = colUK.find(query_b)
    movies_b = [mov for mov in result_b]

    query_c = {"$and": [{"actors": "McAree, Darren"}, {"actors": "Lockett, Katie"}]}
    result_c = colUK.find(query_c)
    movies_c = [mov for mov in result_c]

    movies = [movies_a, movies_b, movies_c]
    return render_template('topUK.html', movies=movies)