# flask_app/models/peluche.py
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Peluche:
    DB = "esquema_peluches"

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.visitas = data['visitas']
        self.usuario_id = data['usuario_id']
        self.adoptador_id = data['adoptador_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.donador = None
        self.adoptador = None

    @classmethod
    def guardar(cls, formulario):
        query = """
            INSERT INTO peluches (nombre, descripcion, usuario_id) 
            VALUES (%(nombre)s, %(descripcion)s, %(usuario_id)s);
        """
        return connectToMySQL(cls.DB).query_db(query, formulario)

    @classmethod
    def obtener_todos(cls):
        query = """
            SELECT peluches.*, usuarios.nombre as donador_nombre 
            FROM peluches 
            JOIN usuarios ON peluches.usuario_id = usuarios.id;
        """
        resultados = connectToMySQL(cls.DB).query_db(query)
        peluches = []
        if resultados:
            for fila in resultados:
                peluche = cls(fila)
                peluche.donador = fila['donador_nombre']
                peluches.append(peluche)
        return peluches

    @classmethod
    def obtener_por_id(cls, data):
        query = """
            SELECT peluches.*, 
                donador.nombre as donador_nombre,
                adoptador.nombre as adoptador_nombre
            FROM peluches 
            JOIN usuarios as donador ON peluches.usuario_id = donador.id
            LEFT JOIN usuarios as adoptador ON peluches.adoptador_id = adoptador.id
            WHERE peluches.id = %(id)s;
        """
        resultado = connectToMySQL(cls.DB).query_db(query, data)
        if resultado:
            fila = resultado[0]
            peluche = cls(fila)
            peluche.donador = fila['donador_nombre']
            peluche.adoptador = fila['adoptador_nombre']
            return peluche
        return False
        
    @classmethod
    def actualizar(cls, formulario):
        query = """
            UPDATE peluches 
            SET nombre=%(nombre)s, descripcion=%(descripcion)s 
            WHERE id=%(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, formulario)

    @classmethod
    def borrar(cls, data):
        query = "DELETE FROM peluches WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def sumar_visita(cls, data):
        query = "UPDATE peluches SET visitas = visitas + 1 WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def adoptar(cls, data):
        query = "UPDATE peluches SET adoptador_id = %(adoptador_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validar_peluche(formulario, es_edicion=False):
        es_valido = True
        if len(formulario['nombre']) < 2:
            flash("El nombre del peluche no puede estar vacío (mínimo 2 letras).", "peluche")
            es_valido = False
        if len(formulario['descripcion']) < 2:
            flash("La descripción no puede estar vacía.", "peluche")
            es_valido = False

        query = "SELECT * FROM peluches WHERE nombre = %(nombre)s;"
        resultado = connectToMySQL(Peluche.DB).query_db(query, formulario)
        
        if resultado:
            if es_edicion and int(resultado[0]['id']) == int(formulario['id']):
                pass # Es el mismo peluche, se permite
            else:
                flash("Este nombre de peluche ya existe en el sistema. ¡Elige uno único!", "peluche")
                es_valido = False
                
        return es_valido