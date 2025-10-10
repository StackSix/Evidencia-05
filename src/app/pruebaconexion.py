# src/app/smoke_db.py
from app.conn.cursor import get_cursor

def main():
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS total_usuarios FROM usuarios;")
        print("✅ Usuarios:", cur.fetchone())
        cur.execute("SELECT COUNT(*) AS total_dispositivos FROM dispositivos;")
        print("✅ Dispositivos:", cur.fetchone())
        cur.execute("SELECT COUNT(*) AS total_automatizaciones FROM automatizaciones;")
        print("✅ Automatizaciones:", cur.fetchone())

if __name__ == "__main__":
    main()
