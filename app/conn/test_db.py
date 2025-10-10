from db_conn import connect_to_mysql

conn = connect_to_mysql()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")
    print("🕒 Fecha y hora del servidor:", cursor.fetchone())
    conn.close()
