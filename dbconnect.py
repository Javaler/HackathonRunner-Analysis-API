import psycopg2
import key

def DBConnect():
    print('DBConnect')
    conn = psycopg2.connect(user=key.user,
                            password=key.password,
                            host=key.host,
                            dbname=key.dbname,
                            sslmode=key.sslmode)
    
    cur = conn.cursor()
    cur.execute('SELECT * FROM post;')
    data = cur.fetchall()
    # 接続を閉じる
    conn.close()

    return data
