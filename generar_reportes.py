import sqlite3
import pandas as pd

def generar_reportes():
    conn = sqlite3.connect('universidad_clean.db')
    # Leer todas las matriculaciones y detalles del alumno y el curso
    df = pd.read_sql_query('''
        SELECT a.nombre AS alumno_nombre, a.apellido AS alumno_apellido, c.nombre AS curso_nombre, m.nota
        FROM matriculaciones m
        JOIN alumnos a ON m.alumno_id = a.id
        JOIN cursos c ON m.curso_id = c.id
    ''', conn)

    # Filtrar aprobados y aplazos
    aprobados = df[df['nota'] >= 60]
    aplazos = df[df['nota'] < 60]

    # Guardar en CSV
    aprobados.to_csv('aprobados.csv', index=False)
    aplazos.to_csv('aplazos.csv', index=False)

    conn.close()

if __name__ == "__main__":
    generar_reportes()
