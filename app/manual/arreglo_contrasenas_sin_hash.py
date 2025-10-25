import bcrypt
import mysql.connector

DB_CONFIG = {
    "host": "bowtbpbberdfnkr3zske-mysql.services.clever-cloud.com",
    "user": "uzxyw8w4coskn9sx",
    "password": "9UJ3mFqPqCJ1659TJVR5",
    "database": "bowtbpbberdfnkr3zske"
}

def reset_admin_password(email_admin, nueva_contrasena):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()

    nuevo_hash = bcrypt.hashpw(nueva_contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    cur.execute("UPDATE usuario SET contrasena = %s WHERE email = %s;", (nuevo_hash, email_admin))
    conn.commit()

    print(f"✅ Contraseña del admin '{email_admin}' actualizada correctamente.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    reset_admin_password("danigonzalez@gmail.com", "123456789")  # Cambia el correo y la contraseña
