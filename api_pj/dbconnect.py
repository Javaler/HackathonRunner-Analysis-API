import psycopg2
import os

def DBConnect():

    conn = psycopg2.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
    
    cur = conn.cursor()
    cur.execute('SELECT * FROM post;')
    data = cur.fetchall()

    return data
