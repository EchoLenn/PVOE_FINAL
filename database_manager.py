import sqlite3
import os

DB_NAME = "escuela.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido_paterno TEXT NOT NULL,
                apellido_materno TEXT,
                direccion TEXT,
                fecha_nacimiento TEXT,
                genero TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tutores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_alumno INTEGER NOT NULL,
                nombre_completo TEXT,
                telefono TEXT,
                correo TEXT,
                FOREIGN KEY(id_alumno) REFERENCES alumnos(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calificaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_alumno INTEGER NOT NULL,
                materia TEXT NOT NULL,
                calificacion REAL,
                FOREIGN KEY(id_alumno) REFERENCES alumnos(id)
            )
        """)

        conn.commit()
        conn.close()
        print("Base de datos inicializada correctamente.")
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")