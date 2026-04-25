import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="phonebook",
        user="postgres",
        password="Ayala2020"
    )