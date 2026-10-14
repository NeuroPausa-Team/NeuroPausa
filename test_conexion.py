from database.conexion import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT NombreRol FROM Rol")
for row in cursor.fetchall():
    print(row)
conn.close()