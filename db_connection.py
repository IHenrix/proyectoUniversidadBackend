import mysql.connector

def get_db_connection(db_config):
    return mysql.connector.connect(**db_config)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'db_universidad'
}