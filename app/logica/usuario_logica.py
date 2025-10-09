import bcrypt
import mysql.connector
from src.conn.db_conn import connect_to_mysql
from src.servicios.broker.menu_broker import menu_principal


def registrar_usuario(nombre, email, password, pregunta_seguridad, respuesta_seguridad):
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT email FROM inversores WHERE email = %s", (email,))
            if cursor.fetchone():
                print("El email ingresado ya está registrado.")
                return

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            cursor.execute(
                "INSERT INTO inversores (nombre, email, contraseña, saldo, pregunta_seguridad, respuesta_seguridad) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    nombre,
                    email,
                    hashed_password,
                    1000000,
                    pregunta_seguridad,
                    respuesta_seguridad,
                ),
            )
            connection.commit()
            print("Usuario registrado con éxito.")

            cursor.execute("SELECT cuit FROM inversores WHERE email = %s", (email,))
            inversor_id = cursor.fetchone()[0]
            menu_principal(inversor_id)
        except Exception as e:
            print(f"Error al registrar el usuario: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("No se pudo conectar a la base de datos.")
