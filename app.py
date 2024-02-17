from flask import Flask, render_template, request, redirect, url_for, session
from Clases.viaje import *

app = Flask(__name__)
app.secret_key = 'asdfholajklñ'


@app.route('/', methods=['GET', 'POST'])
def crearViaje():
    if request.method == 'POST':
        nombre = request.form['nombre']
        numeroIntegrantes = request.form['integrantes']
        latitud = request.form['latitud']
        longitud = request.form['longitud']

        print(latitud, longitud)
        return redirect(url_for('crearIntegrante', integrantes=numeroIntegrantes))
    return render_template('crearViaje.html')

@app.route('/integrantes/<int:integrantes>', methods=['GET', 'POST'])
def crearIntegrante(integrantes):
    return render_template('crearViajero.html', integrantes = integrantes)

@app.route('/viaje', methods=['GET', 'POST'])
def verViaje(viaje):
    return render_template('rutas.html')

if __name__ == '__main__':
    app.run(debug=True)