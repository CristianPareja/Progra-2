import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='inventario_discos',
        user='postgres',
        password='Soysuficiente91*'
    )
    print("Conexión exitosa a la base de datos.")
    conn.close()
except Exception as e:
    print(f"Error en conexión: {e}")
