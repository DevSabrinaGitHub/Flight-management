import sqlite3

def crear_base_datos():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    # Crear la tabla de usuarios para el login
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correo TEXT NOT NULL UNIQUE,
            contraseña TEXT NOT NULL
        )
    ''')
    
    # Insertar un usuario de ejemplo para el login
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (correo, contraseña)
        VALUES ('cuentavuelos@gmail.com', '1234')
    ''')

    # Crear la tabla de pasajeros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pasajeros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            dni TEXT NOT NULL UNIQUE
        )
    ''')

    # Insertar un pasajero de ejemplo
    cursor.execute('''
        INSERT OR IGNORE INTO pasajeros (nombre, apellido, dni)
        VALUES ('Juan', 'Pérez', '45000000')
    ''')

    # Crear la tabla de aviones para el panel de administración
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aviones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT UNIQUE NOT NULL,
            nombre TEXT,
            marca TEXT,
            modelo TEXT,
            asientos_normal INTEGER,
            asientos_turista INTEGER,
            asientos_premium INTEGER,
            kilometraje REAL,
            en_vuelo BOOLEAN
        )
    ''')
    
    # Crear la tabla de vuelos para el panel de administración
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vuelos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            avion_id INTEGER NOT NULL,
            ciudad_origen TEXT NOT NULL,
            ciudad_destino TEXT NOT NULL,
            fecha_partida TEXT NOT NULL,
            fecha_llegada TEXT NOT NULL,
            FOREIGN KEY (avion_id) REFERENCES aviones(id)
        )
    ''')

    # Insertar algunos aviones de ejemplo
    cursor.execute('''
        INSERT OR IGNORE INTO aviones (matricula, nombre, marca, modelo, asientos_normal, asientos_turista, asientos_premium, kilometraje, en_vuelo)
        VALUES ('ABC123', 'Avión Alpha', 'Boeing', '737', 120, 80, 10, 15000, 0),
               ('DEF456', 'Avión Beta', 'Airbus', 'A320', 130, 70, 20, 22000, 1),
               ('GHI789', 'Avión Gamma', 'Boeing', '747', 200, 100, 30, 50000, 0)
    ''')

    conn.commit()
    conn.close()
    print("Base de datos 'usuarios.db' creada y configurada correctamente.")

crear_base_datos()
