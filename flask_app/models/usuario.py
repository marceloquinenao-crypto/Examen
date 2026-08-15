from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

# Expresión para validar el formato de email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    DB = "esquema_peluches"

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Consultas SQL

    @classmethod
    def guardar(cls, formulario):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password) 
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.DB).query_db(query, formulario)

    @classmethod
    def get_by_email(cls, formulario):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultados = connectToMySQL(cls.DB).query_db(query, formulario)
        if len(resultados) < 1:
            return False
        return cls(resultados[0])

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultados = connectToMySQL(cls.DB).query_db(query, formulario)
        if len(resultados) < 1:
            return False
        return cls(resultados[0])

    # Validaciones del Examen
    @staticmethod
    def validar_registro(formulario):
        es_valido = True
        
        if len(formulario['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            es_valido = False
            
        if len(formulario['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            es_valido = False
            
        if not EMAIL_REGEX.match(formulario['email']):
            flash("El formato del email es inválido.", "registro")
            es_valido = False
        else:
            usuario_existente = Usuario.get_by_email({'email': formulario['email']})
            if usuario_existente:
                flash("Este email ya se encuentra registrado.", "registro")
                es_valido = False
                
        if formulario['password'] != formulario['confirmar_password']:
            flash("Las contraseñas no coinciden.", "registro")
            es_valido = False
            
        return es_valido