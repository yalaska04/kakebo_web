from kakebo import app
import sqlite3
from flask import jsonify, render_template


@app.route('/')
def index():
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()
    
    cur.execute("SELECT * FROM movimientos;")
    
    claves = cur.description
    filas = cur.fetchall()
    movimientos = []
    saldo = 0
    
    for fila in filas:
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor
            print(d)
        if d['esGasto'] == 0:
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo
        movimientos.append(d)
    conexion.close()
    return render_template('movimientos.html', datos = movimientos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo(): 
    return render_template('alta.html')