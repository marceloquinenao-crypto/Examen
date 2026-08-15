from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.peluche import Peluche

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    todos_los_peluches = Peluche.obtener_todos()
    return render_template('dashboard.html', peluches=todos_los_peluches)

@app.route('/nueva')
def nueva_donacion():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('nueva.html')

@app.route('/crear_peluche', methods=['POST'])
def crear_peluche():
    if 'usuario_id' not in session:
        return redirect('/')
    if not Peluche.validar_peluche(request.form):
        return redirect('/nueva')
    data = {
        "nombre": request.form['nombre'],
        "descripcion": request.form['descripcion'],
        "usuario_id": session['usuario_id']
    }
    Peluche.guardar(data)
    return redirect('/dashboard')

@app.route('/ver/<int:id>')
def ver_peluche(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    data = {"id": id}
    Peluche.sumar_visita(data)
    peluche_actual = Peluche.obtener_por_id(data)
    return render_template('ver.html', peluche=peluche_actual)

@app.route('/editar/<int:id>')
def editar_peluche(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    data = {"id": id}
    peluche_actual = Peluche.obtener_por_id(data)
    if peluche_actual.usuario_id != session['usuario_id']:
        return redirect('/dashboard')
        
    return render_template('editar.html', peluche=peluche_actual) 

@app.route('/actualizar_peluche/<int:id>', methods=['POST'])
def actualizar_peluche(id):
    if 'usuario_id' not in session:
        return redirect('/')
    data = {
        "id": id,
        "nombre": request.form['nombre'],
        "descripcion": request.form['descripcion']
    }
    
    if not Peluche.validar_peluche(data, es_edicion=True):
        return redirect(f'/editar/{id}')
    Peluche.actualizar(data)
    return redirect('/dashboard')

@app.route('/borrar/<int:id>')
def borrar_peluche(id):
    if 'usuario_id' not in session:
        return redirect('/')
        
    data = {"id": id}
    peluche_actual = Peluche.obtener_por_id(data)
    if peluche_actual.usuario_id == session['usuario_id']:
        Peluche.borrar(data)
    return redirect('/dashboard')

@app.route('/adoptar/<int:id>')
def adoptar_peluche(id):
    if 'usuario_id' not in session:
        return redirect('/')
        
    data = {
        "id": id,
        "adoptador_id": session['usuario_id']
    }
    Peluche.adoptar(data)
    return redirect('/dashboard')