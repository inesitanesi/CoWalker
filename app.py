from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'asdfholajklñ'


@app.route('/', methods=['GET', 'POST'])
def crearViaje():
    return render_template('crearViaje.html')

@app.route('/integrantes', methods=['GET', 'POST'])
def crearIntegrante():
    return render_template('crearViajero.html')

@app.route('/viaje',, methods=['GET', 'POST'])
def verViaje(viaje):
    return render_template('rutas.html')

if __name__ == '__main__':
    app.run(debug=True)