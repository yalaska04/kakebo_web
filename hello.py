from flask import Flask

app = Flask(__name__) # crea una instancia de Flask() (clase aplicación)

@app.route('/') 
def index(): 
    return 'Hola, mundo!'

@app.route('/adiós')
def bye(): 
    return 'Hasta luego, cocodrilo'