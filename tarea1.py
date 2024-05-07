import sqlite3
import pandas as pd

def cargar_datos():
    # Conectar a la base de datos
    conn = sqlite3.connect('universidad_clean.db')
    cursor = conn.cursor()

    # Leer el archivo CSV e iterar sobre las filas
    df = pd.read_csv('dataset/datos.csv')

    # Variable para almacenar el ID del último alumno procesado
    ultimo_alumno_id = None

    for index, row in df.iterrows():
        # Verificar si el alumno actual es diferente del último procesado
        if row['alumno_id'] != ultimo_alumno_id:
            if ultimo_alumno_id is not None:
                # Imprimir una línea de separación si no es el primer registro
                print("-" * 80)
            # Actualizar el último alumno procesado
            ultimo_alumno_id = row['alumno_id']

        # Verificar si el alumno ya existe
        if not cursor.execute('SELECT id FROM alumnos WHERE id=?', (row['alumno_id'],)).fetchone():
            # Insertar el alumno si no existe
            cursor.execute('''
                INSERT INTO alumnos (id, nombre, apellido, fecha_nacimiento)
                VALUES (?, ?, ?, ?)
            ''', (row['alumno_id'], row['nombre'], row['apellido'], row['fecha_nacimiento']))
            print(f"> Alumno insertado: {row['nombre']} {row['apellido']} (ID: {row['alumno_id']}).")

        # Verificar si el curso es válido y obtener el nombre del curso
        curso = cursor.execute('SELECT nombre FROM cursos WHERE id=?', (row['curso_id'],)).fetchone()
        if curso:
            nombre_curso = curso[0]
            # Validar la nota
            if pd.notna(row['nota']) and row['nota'] >= 0:
                # Verificar si la matriculación ya existe
                if not cursor.execute('''
                    SELECT id FROM matriculaciones WHERE curso_id=? AND alumno_id=? AND anho=?
                ''', (row['curso_id'], row['alumno_id'], row['anho'])).fetchone():
                    # Insertar la matriculación si no existe
                    cursor.execute('''
                        INSERT INTO matriculaciones (curso_id, alumno_id, anho, nota)
                        VALUES (?, ?, ?, ?)
                    ''', (row['curso_id'], row['alumno_id'], row['anho'], row['nota']))
                    print(f"Matriculación registrada: {row['nombre']} {row['apellido']} para el curso {nombre_curso} en el año {row['anho']}.")
                else:
                    print(f"Se omitió un registro de matriculación duplicado para {row['nombre']} {row['apellido']} y curso {nombre_curso} en el año {row['anho']}.")
            else:
                # Notificar que la nota es inválida junto con el registro del alumno
                print(f"Nota inválida {row['nota']} para {row['nombre']} {row['apellido']}; matriculación no registrada.")
        else:
            print(f"Curso no válido: ID {row['curso_id']} para el alumno {row['nombre']} {row['apellido']}. Matriculación no registrada")

    # Guardar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    print("\nProceso completado.")

if __name__ == "__main__":
    cargar_datos()
