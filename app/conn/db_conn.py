import mysql.connector

def connect_to_mysql():
    config = {
        "user": "uzxyw8w4coskn9sx",  
        "password": "9UJ3mFqPqCJ1659TJVR5",  
        "host": "bowtbpbberdfnkr3zske-mysql.services.clever-cloud.com",
        "port": 3306,
        "database": "bowtbpbberdfnkr3zske",
        "raise_on_warnings": True,
    }

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("✅ Conexión exitosa a la base de datos.")
        return connection

    except mysql.connector.Error as err:
        print(f"❌ Error al conectar a MySQL: {err}")
        return None
