# CoWalker
# Copyright (c) 2024, Elena Fernández del Sel, Nicolás Fernández Otero, Roberto Tato Lage, Inés Quintana Raña
# SPDX-License-Identifier: MIT


from flask import Flask, render_template, request, redirect, url_for, session
from Clases.viaje import *

app = Flask(__name__)
app.secret_key = 'asdfholajklñ'
viaje = Viaje()

@app.route('/', methods=['GET', 'POST'])
def crearViaje():
    if request.method == 'POST':
        nombre = request.form['nombre']
        numeroIntegrantes = request.form['integrantes']
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        viaje.set_nombre(nombre)
        viaje.set_destino(Nodo("destino", float(latitud), float(longitud)))

        return redirect(url_for('crearIntegrante', integrantes=numeroIntegrantes))
    return render_template('crearViaje.html')

@app.route('/integrantes/<int:integrantes>', methods=['GET', 'POST'])
def crearIntegrante(integrantes):
    if request.method == 'POST':
        for i in range(integrantes):    
            nombre  = request.form[f'nombre{i}']
            latitud = request.form[f'latitud{i}']
            longitud = request.form[f'longitud{i}']
            viaje.agregar_nodo(Nodo(nombre, float(latitud), float(longitud)))
        return redirect(url_for('verViaje'))
    return render_template('crearViajero.html', integrantes = integrantes)

@app.route('/viaje', methods=['GET', 'POST'])
def verViaje():
    viaje.ejecutar()
    return render_template('rutas.html', viaje=viaje)

if __name__ == '__main__':
    app.run(debug=True)