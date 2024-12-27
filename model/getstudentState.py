from templates.config import conn
cur = conn.cursor()


def getstudentState(studentId):
    sql = """
            SELECT ss.state
            FROM studentState as ss
            JOIN studentPasswords as sp ON ss.studentId = sp.studentId
            WHERE sp.username = '%s';
        """ % (studentId)
    cur.execute(sql)
    result = cur.fetchall()
    print(result[0][0])
    return result[0][0]

if __name__ == "__main__":
    state=getstudentState(123)