from flask_wtf import form
from kakebo import app
from flask import jsonify, render_template, request, redirect, url_for, flash
from kakebo.forms import MovimientosForm
from datetime import date

import sqlite3

def consultaSQL(query, parametros = []): 
    # Abrimmos la conexión
    conexion = sqlite3.connect('movimientos.db')
    cur = conexion.cursor()

    # Ejecutamos la consulta
    cur.execute(query, parametros)

    # Obtenemos los datos de la consulta
    claves = cur.description
    filas = cur.fetchall()

    # Procesar los datos para devolver una lista de diccionarios. Un diccionario por fila

    resultado = []
    for fila in filas:
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor
            print(d)
        resultado.append(d)

    conexion.close()
    return resultado

def modificaTablaSQL(query, parametros=[]): 
    conexion = sqlite3.connect('movimientos.db')
    cur = conexion.cursor()

    cur.execute(query, parametros)

    conexion.commit()
    conexion.close()

@app.route('/')
def index():
    movimientos = consultaSQL('SELECT * FROM movimientos order by fecha;') # lista de diccionarios con claves y valores

    saldo = 0
    for d in movimientos:
        if d['esGasto'] == 0:
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo

    return render_template('movimientos.html', datos = movimientos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    formulario = MovimientosForm() 

    if request.method == 'GET': 
        return render_template('alta.html', form = formulario)
    else: 
        if formulario.validate(): 
            query = "INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad) VALUES (?, ?, ?, ?, ?)"
            try: 
                modificaTablaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                                    formulario.esGasto.data, formulario.cantidad.data]) # inyectamos los valores
            
            except sqlite3.Error as el_error: 
                print('Error en SQL INSERT', el_error)
                flash('Se ha producido un error en la base de datos. Pruebe en unos minutos')
                return render_template('alta.html', form= formulario)

            """
            query = "INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad) VALUES (:fecha, :concepto, :categoria, :esGasto, :cantidad)"
            cur.execute(query, {
                'fecha': formulario.fecha.data, 
                'concepto': formulario.concepto.data, 
                'categoria': formulario.categoria.data,
                'esGasto': formulario.esGasto.data, 
                'cantidad':formulario.cantidad.data
            }
            
            """

            return redirect(url_for('index'))

            # Redirect a la ruta /
        else: 
            return render_template('alta.html', form = formulario)

@app.route('/borrar/<int:id>', methods=['GET', 'POST'])
def borrar(id):
    if request.method == 'GET': 
        filas = consultaSQL('SELECT * FROM movimientos WHERE id=?', [id])
        if len(filas) == 0: 
            flash('El resgistro no existe')
            return render_template('borrar.html')
    
        return render_template('borrar.html', movimiento = filas[0])
    
    else: 
        try: 
            modificaTablaSQL('DELETE FROM movimientos WHERE id = ?;', [id])
        except sqlite3.Error as e: 
            flash('Se ha producido un error en la base de datos, vuelva a intentarlo', 'error')
            return redirect(url_for('index')) 
        
        flash('Borrado realizado con éxito', 'aviso')
        return redirect(url_for('index')) 
    

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id): 
    if request.method == 'GET': 
        filas = consultaSQL('SELECT * FROM movimiento WHERE id=?', [id])
        if len(filas) == 0: 
            flash('El registro no existe', 'error')
            return render_template('modificar.html')

        registro = filas[0]
        registro['fecha'] = date.fromisoformat()
        formulario = MovimientosForm(data = registro) 

        return render_template('modificar.html', form = formulario)