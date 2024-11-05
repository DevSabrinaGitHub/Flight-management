import sqlite3

def ejecutar_consulta(query, params=()):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    resultado = cursor.fetchall()
    conn.commit()
    conn.close()
    return resultado
