import sqlite3

DB_NAME = "roomscan.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            metodo_login TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inmuebles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_uso TEXT NOT NULL,
            latitud REAL NOT NULL,
            longitud REAL NOT NULL,
            area REAL NOT NULL,
            volumen REAL NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def guardar_inmueble(nombre, tipo_uso, latitud, longitud, area, volumen):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO inmuebles (nombre, tipo_uso, latitud, longitud, area, volumen)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombre, tipo_uso, latitud, longitud, area, volumen))
    conn.commit()
    conn.close()

def obtener_inmuebles():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, tipo_uso, latitud, longitud, area, volumen FROM inmuebles ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def obtener_resumen_metricas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(area), SUM(volumen) FROM inmuebles")
    total, total_area, total_volumen = cursor.fetchone()
    conn.close()
    return {
        "totales": total or 0,
        "area_mapeada": round(total_area or 0.0, 2),
        "volumen_3d": round(total_volumen or 0.0, 2)
    }

def limpiar_base_datos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inmuebles")
    conn.commit()
    conn.close()