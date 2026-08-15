from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario

# Bcrypt para encriptar contraseñas
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    password_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password": password_hash
    }

    id_usuario = Usuario.guardar(data)
    session['usuario_id'] = id_usuario
    session['nombre'] = request.form['nombre']
    
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form['email']}
    usuario_db = Usuario.get_by_email(data)
    
    if not usuario_db:
        flash("Email no encontrado.", "login")
        return redirect('/')
        
    if not bcrypt.check_password_hash(usuario_db.password, request.form['password']):
        flash("Contraseña incorrecta.", "login")
        return redirect('/')
        
    session['usuario_id'] = usuario_db.id
    session['nombre'] = usuario_db.nombre
    
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')