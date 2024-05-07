import sqlite3

def limpiar_datos():
    conn = sqlite3.connect('universidad_clean.db')
    cursor = conn.cursor()

    # Borrar datos de las tablas
    cursor.execute('DELETE FROM matriculaciones')
    cursor.execute('DELETE FROM alumnos')

    conn.commit()
    conn.close()
    print("Base de datos limpiada con éxito.")

if __name__ == "__main__":
    limpiar_datos()
