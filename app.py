#!/usr/bin/env python
# coding=utf-8

import csv
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_bootstrap import Bootstrap
# from flask_moment import Moment
from flask_script import Manager
from forms import LoginForm, SaludarForm, RegistrarForm
import funciones

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
# moment = Moment(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'


@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())


@app.route('/saludar', methods=['GET', 'POST'])
def saludar():
    formulario = SaludarForm()
    if formulario.validate_on_submit():
        print(formulario.usuario.name)
        return redirect(url_for('saludar_persona', usuario=formulario.usuario.data))
    return render_template('saludar.html', form=formulario)


@app.route('/saludar/<usuario>')
def saludar_persona(usuario):
    return render_template('usuarios.html', nombre=usuario)


@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)


@app.route('/secret', methods=['GET'])
def secreto():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        return render_template('sin_permiso.html')


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))

################################ VER CSV ###############################
@app.route('/vercsv', methods=['GET'])
def vercsv():
    with open('datos.csv', 'r') as f:
      reader = csv.reader(f)
      vercontenido = list(reader)
      return render_template("vercsv.html", tabla=vercontenido)
################################ VER CSV ###############################

############################ ULTIMAS VENTAS ############################
@app.route('/ultimasventas', methods=['GET'])
def ultimasventas():
    with open('datos.csv', 'r') as f:
      reader = csv.reader(f)
      next(reader)
      vercontenido = list(reader)
      return render_template("ultimasventas.html", tabla=vercontenido)
############################ ULTIMAS VENTAS ############################

######################### PRODUCTOS POR CLIENTE ########################
@app.route('/producliente', methods=['GET', 'POST'])
def producliente():
    formulario = SaludarForm()
    if formulario.validate_on_submit(): #va por POST
        print("POST")
        cliente = formulario.usuario.data
        ventas = funciones.loadcsv("datos.csv")
        if ventas is None:
            print("Error de carga.")
        productos = funciones.productosPorCliente(ventas, cliente)
        print(productos)
        print(cliente)

        return render_template('listado.html', lista=productos)
    else:
        #flash('Revisá el nombre del cliente.')
        #return redirect(url_for('producliente'))
        return render_template('producliente.html', form=formulario)
######################### PRODUCTOS POR CLIENTE ########################


######################### CLIENTE POR PRODUCTOS ########################
@app.route('/clienteprodu', methods=['GET', 'POST'])
def clienteprodu():
    formulario = SaludarForm()
    if formulario.validate_on_submit(): #va por POST
        print("POST")
        cliente = formulario.usuario.data
        ventas = funciones.loadcsv("datos.csv")
        if ventas is None:
            print("Error de carga.")
        productos = funciones.clientesPorProducto(ventas, cliente)
        print(productos)
        print(cliente)

        return render_template('listado.html', lista=productos)
    else:
        #flash('Revisá el nombre del cliente.')
        #return redirect(url_for('producliente'))
        return render_template('clienteprodu.html', form=formulario)
######################### CLIENTE POR PRODUCTOS ########################


######################### PRODUCTO MAS VENDIDO #########################

######################### PRODUCTO MAS VENDIDO #########################


########################## CLIENTE POR GASTOS ##########################
#consulta por dinero gastado por cada cliente

########################## CLIENTE POR GASTOS ##########################


if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True)
    manager.run()
