#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from email.policy import default
import logging
from pickle import NONE
import random
import traceback
from app import app
from flask import render_template, request, url_for, redirect, session
import hashlib
import json
import os
import sys
import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if "carrito" not in session:
        session["carrito"] = []
        session.modified = True

    inventario_data = open(os.path.join(app.root_path,'inventario/inventario.json'), encoding="utf-8").read()
    inventario = json.loads(inventario_data)
    inventarioSearch = []
    inventarioSearchv2 = []
    if 'categorias' in request.form:
        if request.form['categorias'] == "":
             if 'titulo' in request.form:
                if request.form['titulo'] == "":
                    return render_template('index.html', title = "Home", movies=inventario['peliculas'])
                for i in inventario['peliculas']:
                    if request.form['titulo'] in i['titulo'] :
                        inventarioSearch.append(i)
                return render_template('index.html', title = "Home", movies=inventarioSearch)
        for i in inventario['peliculas']:
            if i['categoria'] == request.form['categorias']:
                inventarioSearch.append(i)
        if 'titulo' in request.form:
            if request.form['titulo'] == "":
                return render_template('index.html', title = "Home", movies=inventarioSearch)
            for i in inventarioSearch:
                if request.form['titulo'] in i['titulo'] :
                    inventarioSearchv2.append(i)
            return render_template('index.html', title = "Home", movies=inventarioSearchv2)
        return render_template('index.html', title = "Home", movies=inventarioSearch)
    return render_template('index.html', title = "Home", movies=inventario['peliculas'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if ('username' in request.form):
        print(request.form['username'])
        # aqui se deberia validar con fichero .dat del usuario
        path = os.path.join(app.root_path, "si1users")
        path = os.path.join(path, str(request.form['username']))
        print(path)
        if os.path.exists(path):

            print ("HOLLAAA", file=sys.stderr)
            path = os.path.join(path, "userdata.json")
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data["contrasena"] == hashlib.sha3_384(request.form['password'].encode('utf-8')).hexdigest():
                    session['saldo'] = data['saldo']
                    session['usuario'] = request.form['username']
                    session.modified=True
                    # se puede usar request.referrer para volver a la pagina desde la que se hizo login
                    return redirect(url_for('index'))
                else:
                    # aqui se le puede pasar como argumento un mensaje de login invalido
                    return render_template('login.html', title = "Sign In")
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
    session.pop('saldo', None)
    return redirect(url_for('index'))


@app.route('/almacen<id>', methods=["GET", "POST"])
def almacen(id):
    nota = "No has valorado esta peli"

    if "nota" in request.form:

        path = os.path.join(app.root_path, 'inventario/inventario.json')


        inventario_data = open(path).read()
        with open(path, "w") as output:
            config = json.loads(inventario_data)
            for i in config['peliculas']:
                if int(i['id']) == int(id):
                    movie_id = i
                    break
            flag = 0
            for i in config["peliculas"][movie_id["id"]-1]["valoraciones"]:
                if i["user"] == session['usuario']:
                    i['valoracion'] = int(request.form['nota'])
                    flag = 1
                    break
            if flag == 0:
                val = {"user": session['usuario'], "valoracion": int(request.form['nota'])}
                config["peliculas"][movie_id["id"]-1]["valoraciones"].append(val)
            output.seek(0)        # <--- should reset file position to the beginning.
            json.dump(config, output)
            output.truncate()     # remove remaining part
        
        nota = request.form['nota']
        average = 0 
        k = 0
        for j in movie_id['valoraciones']:
            average += j['valoracion']
            k += 1
            break
        try:
            average = average / k
        except:
            average = 0
        
        stock = movie_id['stock']
        return render_template('peliculas.html', title="almacen" + id, movie=movie_id, valoracion=round(average), opinion=nota, stock = stock)
       
    nota = -1
    inventario_data = open(os.path.join(
        app.root_path, 'inventario/inventario.json'), encoding="utf-8").read()
    inventario = json.loads(inventario_data)
    for i in inventario['peliculas']:
        if int(i['id']) == int(id):
            movie_id = i
            average = 0
            k = 0
            for j in i['valoraciones']:
                average += j['valoracion']
                k += 1
            break
    try:
        average = average / k
    except:
        average = 0
    if "usuario" in session: 
        for i in inventario["peliculas"][movie_id["id"]-1]["valoraciones"]:
                if i["user"] == session['usuario']:
                    nota = i['valoracion']
                    break
    if "valor" in request.form:

        try:
            if int(request.form['valor']) > 0: 
                pelicula = movie_id
                stock = movie_id['stock']
                for i in session["carrito"]:
                    if i['id'] == movie_id['id']:
                        i["pedidos"] += int(request.form["valor"])
                        return render_template('peliculas.html', title="almacen" + id, movie=movie_id, valoracion=round(average), opinion=nota, stock = stock)
                if "carrito" not in session:
                    session["carrito"] = []
                    session.modified = True
                pelicula["pedidos"] = int(request.form["valor"])
                session["carrito"].append(pelicula)
        except:
            pass
    stock = movie_id['stock']
    return render_template('peliculas.html', title="almacen" + id, movie=movie_id, valoracion=round(average), opinion=nota, stock = stock)
    
@app.route('/singup',methods=["GET", "POST"])
def singup():
    if "submit_button" in request.form:
        dict = {}
        directory = request.form['user']
        parent_dir = app.root_path
        parent_dir = os.path.join(parent_dir, 'si1users')
        path = os.path.join(parent_dir, directory)
        if(os.path.exists(path) == True):
            return render_template('singup.html', error = True)
        os.mkdir(path)
        os.chmod(path, 0o777)
        dict["user"] = request.form['user']
        dict["email"] = request.form['email']
        dict["contrasena"] = hashlib.sha3_384(request.form['contraseña'].encode('utf-8')).hexdigest()
        dict["tarjeta"] = request.form['tarjeta']
        dict["direccion"] = request.form['direccion']
        dict["saldo"] = random.randint(0,50)
        path_2 = os.path.join(path, "userdata.json")
        f = open (path_2, 'w', encoding='utf-8') 
        os.chmod(path_2, 0o777)
        f.close()
        with open (path_2, 'w', encoding='utf-8') as fp:
            json.dump(dict, fp)

        path_2 = os.path.join(path, "compras.json")
        f = open (path_2, 'w', encoding='utf-8') 
        
        os.chmod(path_2, 0o777)
        f.close()
        return redirect(url_for('index'), )
    return render_template('singup.html', error = False) 

@app.route('/carrito', methods=["GET", "POST"])
def carrito():
        id = int(request.args.get('id',None))
        for i in range(len(session["carrito"])):
            if session["carrito"][i]["id"] == id:
                session["carrito"].pop(i)
                break
        if "carrito" in session:
            data = session["carrito"]
            if len(data) == 0:
                return render_template('carrito.html', datos=None, check = 0)
            
            price = 0 
            for item in data:
                price = price + (item["precio"] * item["pedidos"]) 

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