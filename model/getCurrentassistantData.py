from templates.config import conn
cur = conn.cursor()

# 获取招生简章里的学科信息
def getSubject():
    sql = """
    SELECT DISTINCT
    CONCAT(s.subID, s.subName) AS subInfo
	FROM
		currentassistant ca
	JOIN
		major m ON ca.majID = m.majID
	JOIN
		subject s ON m.subID = s.subID
    ORDER BY
        subInfo;
    """
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
    return result
# 获取专业信息
def getMajor():
    sql = """
        SELECT 
            CONCAT(s.subID, s.subName) AS subInfo, 
            CONCAT(ca.majID, ca.majName) AS majInfo, 
            t.teacherName,
            m.majorExamsub
        FROM 
            currentassistant ca
        JOIN 
            major m ON ca.majID = m.majID
        JOIN 
            subject s ON m.subID = s.subID
        JOIN 
            teacher t ON ca.teacherID = t.teacherID
        ORDER BY 
            subInfo,  -- 先按subInfo排序
            majInfo;  -- 在subInfo相同的记录中，再按majInfo排序
        """
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
    return result

def getNeedStudent():
    sql = ("SELECT sum(needstudent) FROM currentassistant")
    cur.execute(sql)
    result = cur.fetchall()
    need_result = result[0][0] if result else 0
    print(need_result)
    return need_result

# 获取学科备注
def getSubjectNote():
    sql = ("SELECT CONCAT(subID,' ', subName,' ', subjectnote) as subjectnote FROM subject")
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
    return result
# 获取专业备注
def getMajorNote():
    sql = ("SELECT majornote FROM major")
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
    return result

if __name__ == "__main__":
    subjects = getSubject()
    majors = getMajor()
    needstudents = getNeedStudent()
    subjectnotes = getSubjectNote()
    majornotes = getMajorNote()
