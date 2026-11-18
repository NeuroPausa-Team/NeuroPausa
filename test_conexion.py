from database.conexion import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT idrol, nombrerol FROM rol;")
print(cursor.fetchall())
conn.close()
