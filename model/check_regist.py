from templates.config import conn

cur = conn.cursor()

def add_user(username, password):
    # sql commands
    sql = "INSERT INTO studentPasswords(username, password) VALUES ('%s','%s')" %(username, password)
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.close()
