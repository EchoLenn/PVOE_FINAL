import sqlite3
import hashlib

DB_NAME = "escuela.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("CREATE TABLE IF NOT EXISTS alumnos (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, apellido_paterno TEXT NOT NULL, apellido_materno TEXT, direccion TEXT, fecha_nacimiento TEXT, genero TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS tutores (id INTEGER PRIMARY KEY, id_alumno INTEGER NOT NULL UNIQUE, nombre_completo TEXT, telefono TEXT, correo TEXT, FOREIGN KEY(id_alumno) REFERENCES alumnos(id) ON DELETE CASCADE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS grupos (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE, profesor TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS materias (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, rol TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS calificaciones (id INTEGER PRIMARY KEY, id_alumno INTEGER NOT NULL, materia TEXT NOT NULL, calificacion REAL, FOREIGN KEY(id_alumno) REFERENCES alumnos(id) ON DELETE CASCADE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS grupo_materias (id_grupo INTEGER, id_materia INTEGER, PRIMARY KEY(id_grupo, id_materia), FOREIGN KEY(id_grupo) REFERENCES grupos(id) ON DELETE CASCADE, FOREIGN KEY(id_materia) REFERENCES materias(id) ON DELETE CASCADE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS inscripciones (id INTEGER PRIMARY KEY, id_alumno INTEGER NOT NULL, id_grupo INTEGER NOT NULL, fecha TEXT, costo REAL, FOREIGN KEY(id_alumno) REFERENCES alumnos(id) ON DELETE CASCADE, FOREIGN KEY(id_grupo) REFERENCES grupos(id) ON DELETE CASCADE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS horarios (id INTEGER PRIMARY KEY, id_grupo INTEGER NOT NULL, materia TEXT NOT NULL, dia TEXT NOT NULL, hora TEXT NOT NULL, UNIQUE(id_grupo, dia, hora), FOREIGN KEY(id_grupo) REFERENCES grupos(id) ON DELETE CASCADE)")
    conn.commit()
    conn.close()

def crear_admin_por_defecto():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE rol = 'admin'")
    if not cursor.fetchone():
        password_hash = hashlib.sha256("1234".encode()).hexdigest()
        cursor.execute("INSERT INTO usuarios (username, password_hash, rol) VALUES (?, ?, ?)", ("admin", password_hash, "admin"))
        conn.commit()
    conn.close()

def verificar_usuario(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT rol FROM usuarios WHERE username = ? AND password_hash = ?", (username, password_hash))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def crear_usuario(username, password, rol):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO usuarios (username, password_hash, rol) VALUES (?, ?, ?)", (username, password_hash, rol))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return "integridad"
    finally:
        conn.close()

def registrar_alumno(datos_alumno, datos_tutor):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alumnos (nombre, apellido_paterno, apellido_materno, direccion, fecha_nacimiento, genero) VALUES (?, ?, ?, ?, ?, ?)", (datos_alumno['nombre'], datos_alumno['apellido_paterno'], datos_alumno['apellido_materno'], datos_alumno['direccion'], datos_alumno['fecha_nacimiento'], datos_alumno['genero']))
    nuevo_id_alumno = cursor.lastrowid
    cursor.execute("INSERT INTO tutores (id_alumno, nombre_completo, telefono, correo) VALUES (?, ?, ?, ?)", (nuevo_id_alumno, datos_tutor['nombre_completo'], datos_tutor['telefono'], datos_tutor['correo']))
    conn.commit()
    conn.close()
    return nuevo_id_alumno

def verificar_alumno_existente(id_alumno):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM alumnos WHERE id = ?", (id_alumno,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def obtener_calificaciones(id_alumno):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT materia, calificacion FROM calificaciones WHERE id_alumno = ?", (id_alumno,))
    calificaciones = cursor.fetchall()
    conn.close()
    return calificaciones

def guardar_calificaciones(id_alumno, lista_calificaciones):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calificaciones WHERE id_alumno = ?", (id_alumno,))
    for materia, calificacion in lista_calificaciones:
        try: calif_float = float(calificacion) if calificacion and calificacion.strip() else None
        except ValueError: calif_float = None
        cursor.execute("INSERT INTO calificaciones (id_alumno, materia, calificacion) VALUES (?, ?, ?)", (id_alumno, materia, calif_float))
    conn.commit()
    conn.close()
    return True

def agregar_grupo_con_materias(nombre, profesor, materias):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO grupos (nombre, profesor) VALUES (?, ?)", (nombre, profesor))
        id_grupo = cursor.lastrowid
        for materia_nombre in materias:
            cursor.execute("INSERT OR IGNORE INTO materias (nombre) VALUES (?)", (materia_nombre,))
            cursor.execute("SELECT id FROM materias WHERE nombre = ?", (materia_nombre,))
            id_materia = cursor.fetchone()[0]
            cursor.execute("INSERT INTO grupo_materias (id_grupo, id_materia) VALUES (?, ?)", (id_grupo, id_materia))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return "integridad"
    finally:
        conn.close()

def obtener_grupos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM grupos ORDER BY nombre")
    grupos = cursor.fetchall()
    conn.close()
    return grupos

def agregar_inscripcion(id_alumno, id_grupo, fecha, costo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inscripciones (id_alumno, id_grupo, fecha, costo) VALUES (?, ?, ?, ?)", (id_alumno, id_grupo, fecha, costo))
    conn.commit()
    conn.close()
    return True

def obtener_historial_inscripciones():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, a.nombre, a.apellido_paterno, g.nombre, i.fecha, i.costo
        FROM inscripciones i JOIN alumnos a ON i.id_alumno = a.id JOIN grupos g ON i.id_grupo = g.id
        ORDER BY i.fecha DESC """)
    historial = cursor.fetchall()
    conn.close()
    return historial

def obtener_alumnos_por_grupo(id_grupo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, a.nombre, a.apellido_paterno, a.apellido_materno
        FROM alumnos a INNER JOIN inscripciones i ON a.id = i.id_alumno WHERE i.id_grupo = ? """, (id_grupo,))
    alumnos = cursor.fetchall()
    conn.close()
    return alumnos

def obtener_materias_por_grupo(id_grupo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.nombre FROM materias m JOIN grupo_materias gm ON m.id = gm.id_materia
        WHERE gm.id_grupo = ? """, (id_grupo,))
    materias = [row[0] for row in cursor.fetchall()]
    conn.close()
    return materias

def guardar_horario(id_grupo, datos_horario):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM horarios WHERE id_grupo = ?", (id_grupo,))
    cursor.executemany("INSERT INTO horarios (id_grupo, dia, hora, materia) VALUES (?, ?, ?, ?)", datos_horario)
    conn.commit()
    conn.close()
    return True

def obtener_horario(id_grupo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dia, hora, materia FROM horarios WHERE id_grupo = ?
        ORDER BY CASE dia WHEN 'Lunes' THEN 1 WHEN 'Martes' THEN 2 WHEN 'Miércoles' THEN 3
        WHEN 'Jueves' THEN 4 WHEN 'Viernes' THEN 5 END, hora
    """, (id_grupo,))
    horario = cursor.fetchall()
    conn.close()
    return horario