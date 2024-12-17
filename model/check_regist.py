from templates.config import conn

cur = conn.cursor()

def add_user(username, password, studentID, studentName, studentIDnumber, studentPhone):
    # sql commands
    sql = "INSERT INTO studentPasswords(username, password, studentID, studentName, studentIDnumber, studentPhone) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (username, password, studentID, studentName, studentIDnumber, studentPhone)
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()

