from templates.config import conn
cur = conn.cursor()
def is_null(username,password):
	if(username==''or password==''):
		return True
	else:
		return False


def is_existed_teacher(username,password):
	sql="SELECT * FROM teacherPasswords WHERE username ='%s' and password ='%s'" %(username,password)
	cur.execute(sql)
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True

def exist_user_teacher(username):
	sql = "SELECT * FROM teacherpasswords WHERE username ='%s'" % (username)
	cur.execute(sql)
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True

def is_existed_student(username,password):
	sql="SELECT * FROM studentPasswords WHERE username ='%s' and password ='%s'" %(username,password)
	cur.execute(sql)
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True

def exist_user_student(username):
	sql = "SELECT * FROM studentpasswords WHERE username ='%s'" % (username)
	cur.execute(sql)
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True

def is_existed_admin(username,password):
	sql="SELECT * FROM admin WHERE username ='%s' and password ='%s'" %(username,password)
	cur.execute(sql)
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True

def exist_user_admin(username):
	sql = "SELECT * FROM admin WHERE username ='%s'" % (username)
	cur.execute(sql)
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True
