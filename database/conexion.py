import pyodbc

def get_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=DESKTOP-9LCD1P8;'
        'DATABASE=NeuroPausaDB;'
        'Trusted_Connection=yes;'
    )
    return conn