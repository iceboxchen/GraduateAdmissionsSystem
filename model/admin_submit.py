from templates.config import conn

cur = conn.cursor()
def is_null_submit(studentID, year, Firstscore, Englishscore, Facescore, Majorscore):
	if(studentID == '' or year == '' or Firstscore == '' or Englishscore == '' or Facescore == '' or Majorscore == ''):
		return True
	else:
		return False


def admin_submit(studentID, year, Firstscore, Englishscore, Facescore, Majorscore):
    # sql commands
    sql = "INSERT INTO score(studentID, year, Firstscore, Englishscore, Facescore, Majorscore) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (studentID, year, Firstscore, Englishscore, Facescore, Majorscore)
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
