import psycopg2
from . import key

def DBConnect():

    conn = psycopg2.connect(
            host=key.host,
            user=key.user,
            password=key.password,
            database=key.database
        )
    
    cur = conn.cursor()
    cur.execute('SELECT * FROM post;')
    data = cur.fetchall()

    return data
