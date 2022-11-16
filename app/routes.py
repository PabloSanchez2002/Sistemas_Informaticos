#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from email.policy import default
import logging
from pickle import NONE
import random
import traceback
from app import app
from flask import render_template, request, url_for, redirect, session
from app import database
import hashlib
import json
import os
import sys
import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    show_movies=database.db_initMovies()
    return render_template('index.html', title = "Home", movies=show_movies)
@app.route('/bestmovies', methods=['GET', 'POST'])
def bestmovies():
    topMovies=[]

    if 'year1' in request.form and 'year2' in request.form:
        try:
            topMovies = database.db_topMovies(request.form['year1'], request.form['year2'], int(request.form['max'])) 
        except:
            topMovies = database.db_topMovies(request.form['year1'], request.form['year2'], 10) 
    return render_template('bestmovies.html', title = "Home", top=topMovies)
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if ('username' in request.form):
        print(request.form['username'])
        # aqui se deberia validar con fichero .dat del usuario
        password = database.db_getPassword(request.form['username'])
        if len(password) != 0 and (password[0][0] == request.form['password'] or hashlib.sha3_384(request.form['password'].encode('utf-8')).hexdigest() == password[0][0]):
            session['saldo'] = password[0][1]
            session['usuario'] = request.form['username']
            session['userid'] = password[0][2]
            session.modified=True
            flag = database.db_checkCarrito(password[0][2])
            if flag == 0:
                #no hay carrito del usuario
                order=database.db_createCarrito(password[0][2])
                if 'carrito' in session:
                    for i in session['carrito']:
                        database.db_insertCarrito(i, order)
                    session.pop('carrito', None)
            else:
                if 'carrito' in session:
                    for i in session['carrito']:
                        print(i)
                        database.db_updateCarrito(i,password[0][2])
                    session.pop('carrito', None)

            # se puede usar request.referrer para volver a la pagina desde la que se hizo login
            return redirect(url_for('index'))
        else:
            # se puede guardar la pagina desde la que se invoca 
            session['url_origen']=request.referrer
            session.modified=True        
            # print a error.log de Apache si se ejecuta bajo mod_wsgi
            print ("ADIOSSS", file=sys.stderr)
            return render_template('login.html', title = "Sign In")
    else:
        # se puede guardar la pagina desde la que se invoca 
        session['url_origen']=request.referrer
        session.modified=True        
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print (request.referrer, file=sys.stderr)
        return render_template('login.html', title = "Sign In")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    session.pop('carrito', None)
    session.pop('userid', None)
    session.pop('saldo', None)
    return redirect(url_for('index'))


@app.route('/almacen<id>', methods=["GET", "POST"])
def almacen(id):
    if "nota" in request.form:
        database.db_actMovie(id, session['userid'], request.form['nota'])
    movie_found=database.db_getMovie(id)
    genres = database.db_getGenres(id)
    price = database.db_getPrice(id)
    print(genres)
    print(price)
    #Obtener valoracion
    if "tipopelicula" in request.form:
        if request.form['tipopelicula'] != -1:
            index = int(int(request.form['tipopelicula']) - 1)
            if 'usuario' in session:
                database.db_addMovie(session['userid'], price[index][2], price[index][1])
                pass
            else: 
                if 'carrito' not in session:
                   session["carrito"] = []
                   session.modified = True
                for i in session['carrito']:
                    if i['prod_id'] == price[index][2]:
                        i['quantity'] += 1
                        return redirect(url_for('index'))
                dict = {}
                dict['prod_id'] = price[index][2]
                dict['movietitle'] = movie_found[0][0][0]
                dict['price'] = price[index][1]
                dict['quantity'] = 1
                session['carrito'].append(dict)
                print(dict)
                return redirect(url_for('index'))

                    

    return render_template('peliculas.html',title="almacen" + id,id= movie_found[0][0][1],genre=genres,prices=price, directors=movie_found[2], actors=movie_found[1], movietitle=movie_found[0][0][0], valoracion=movie_found[0][0][2], opinion=0, stock = movie_found[0][0][3])
    
@app.route('/singup',methods=["GET", "POST"])
def singup():
    if "submit_button" in request.form:
        dict = {}
        dict["user"] = request.form['user']
        dict["email"] = request.form['email']
        dict["contrasena"] = hashlib.sha3_384(request.form['contraseña'].encode('utf-8')).hexdigest()
        dict["tarjeta"] = request.form['tarjeta']
        dict["direccion"] = request.form['direccion']
        dict["saldo"] = random.randint(0,50)
        flag = database.db_createUser(dict)
        if flag == 1:
            return render_template('singup.html', error = True) 
        return redirect(url_for('index'), )
    return render_template('singup.html', error = False) 

@app.route('/carrito', methods=["GET", "POST"])
def carrito():
    if "carrito" in session:
        id = int(request.args.get('id',None))
        for i in range(len(session["carrito"])):
            if session["carrito"][i]["prod_id"] == id:
                session["carrito"].pop(i)
                break
        data = session["carrito"]
        if len(data) == 0:
            return render_template('carrito.html', datos=None, check = 0)

        price = 0 
        for item in data:
            price = price + (item["price"] * item["quantity"]) 
        return render_template('carrito.html', datos=data, check = 1, precio = ("%.2f" % price))
    elif "usuario" in session:
        carrito = database.db_getCarrito(session['userid'])
        data = []
        for i in carrito:
            dict = {} 
            dict['prod_id'] = i[0]
            dict['movietitle'] = i[1] 
            dict['price'] = i[2] 
            dict['quantity'] =  i[3] 
            data.append(dict) 

        if len(data) == 0:
            return render_template('carrito.html', datos=None, check = 0)

        price = 0 
        for item in data:
            price = price + (item["price"] * item["quantity"]) 
        
        return render_template('carrito.html', datos=data, check = 1, precio = ("%.2f" % price))
    return render_template('carrito.html', datos=None, check = 0, precio = None)

@app.route('/pagar', methods=["GET", "POST"])
def pagar():
        inventario_data = open(os.path.join(app.root_path,'inventario/inventario.json'), encoding="utf-8").read()
        inventario = json.loads(inventario_data)
        new_total = 0
        if "usuario" in session:
            if "carrito" in session:

                for i in session["carrito"]:
                    if i["pedidos"] > inventario["peliculas"][i["id"]-1]["stock"]:
                        i["pedidos"] = inventario["peliculas"][i["id"] -1]["stock"]
                        i["modificado"] = True
                    else:
                        i["modificado"] = False
                    new_total += i["pedidos"] * i["precio"]

                i["total"] = new_total 
                #print("Hola")
                if 'pagar' in request.form:
                    #print("ADios")
                    if int(session["saldo"]) >= new_total:
                        parent_dir = app.root_path
                        parent_dir = os.path.join(parent_dir, 'si1users')
                        path = os.path.join(parent_dir, session["usuario"])
                        path = os.path.join(path, "userdata.json")
                        #print(path)
                        user_data = open(path, encoding="utf-8").read()
                        data = json.loads(user_data)
                        data["saldo"] = data["saldo"] - new_total
                        session["saldo"] = data["saldo"]
                        session.modified = True
                        with open (path, 'w', encoding='utf-8') as fp:
                            json.dump(data, fp)

                        for i in session["carrito"]:
                            inventario["peliculas"][i["id"] -1]["stock"] -= i["pedidos"]

                        parent_dir = app.root_path
                        parent_dir = os.path.join(parent_dir, 'inventario/inventario.json')
                        
                        with open (parent_dir, 'w', encoding='utf-8') as fp:
                            json.dump(inventario, fp)

                        parent_dir = app.root_path
                        parent_dir = os.path.join(parent_dir,'si1users')
                        parent_dir = os.path.join(parent_dir,session["usuario"])
                        path = os.path.join(parent_dir,"compras.json")
                        compras_data = open(path, encoding="utf-8").read()

                        
                        try:
                            data_compras= json.loads(compras_data) #en el caso de que sea el primer pedido dara error al abrir el archivo
                        except Exception as e:
                            logging.error(traceback.format_exc())
                            data_compras = {'compras':[]}

                        dict = {}
                        total = 0
                        dict["fecha"] = datetime.datetime.now()
                        dict["pelis"] = []
                        
                        i = 0
                        for peli in session["carrito"]:
                            print(peli)
                            a = {"id" : peli["id"], "titulo" : peli["titulo"], "pedidos" : peli["pedidos"]}
                            dict["pelis"].append(a)
                            
                            total += peli['precio'] * peli['pedidos']
                        dict["sumatotal"] = total
                        data_compras['compras'].append(dict)
                        with open (path, 'w', encoding='utf-8') as fp:
                            json.dump(data_compras, fp, default = str)

                        session.pop("carrito", None)
                        session.modified = True
                        
                        return render_template('historial.html', data = data_compras, pagado = True)
                    else:
                        return render_template('pagar.html', total = ("%.2f" % new_total), error=True)
                return render_template('pagar.html', total = ("%.2f" % new_total), error = False)

@app.route('/historial')
def historial():
    if 'usuario' in session:
        path = os.path.join(app.root_path, "si1users")
        path = os.path.join(path, str(session['usuario']))
        path = os.path.join(path, "compras.json")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return render_template('historial.html', data=data, pagado = False)
    return render_template('index.html')