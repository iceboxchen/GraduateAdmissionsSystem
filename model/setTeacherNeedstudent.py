from templates.config import conn
cur = conn.cursor()

def setTeacherNeedstudent(need):
    query = """
    UPDATE teacherqualification
    SET needstudent = '%s'
    WHERE teacherID = 1
    """%(need)

    cur.execute(query)
    conn.commit()
    cur.close()
