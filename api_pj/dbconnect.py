import psycopg2
import os

def DBConnect():
    print('DBConnect')
    conn = psycopg2.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database=os.environ.get('DATABASE')
        )
    
    cur = conn.cursor()
    cur.execute('SELECT * FROM post;')
    data = cur.fetchall()

    return data
