# Opción A (recomendada): import desde el paquete
from conn.cursor import get_cursor

def main():
    with get_cursor() as cur:
        cur.execute("SELECT NOW() AS fecha_actual;")
        print("✅ Resultado:", cur.fetchone())

if __name__ == "__main__":
    main()
