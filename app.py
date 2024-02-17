from flask import Flask, render_template, request, redirect, url_for, session
from Clases.viaje import *
from Clases.clases import *

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
        viaje.set_destino(Nodo("destino", latitud, longitud))

        return redirect(url_for('crearIntegrante', integrantes=numeroIntegrantes))
    return render_template('crearViaje.html')

@app.route('/integrantes/<int:integrantes>', methods=['GET', 'POST'])
def crearIntegrante(integrantes):
    if request.method == 'POST':
        for i in range(integrantes):                        
            viaje.agregar_nodo(Nodo(request.form[f'nombre{i}'],request.form[f'latitud{i}'],request.form[f'longitud{i}']))

        return redirect(url_for('viaje'))
    return render_template('crearViajero.html', integrantes = integrantes)

@app.route('/viaje', methods=['GET', 'POST'])
def verViaje():
    
    return render_template('rutas.html')

if __name__ == '__main__':
    app.run(debug=True)