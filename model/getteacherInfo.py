from templates.config import conn
cur = conn.cursor()

class TeacherInfo:
    def __init__(self, teacherName, teacheracademyname, teachermajors, teacherTitle, teacherExperience,
                 teacherDirection):
        self.teacherName = teacherName
        self.teacheracademyname = teacheracademyname
        self.teachermajors = teachermajors  # 注意：这里应该是一个列表或其他适当的集合类型
        self.teacherTitle = teacherTitle
        self.teacherExperience = teacherExperience
        self.teacherDirection = teacherDirection

def getteacherInfo(id):
    sql = """
            SELECT teacherName, academyname as teacheracademyname, teacherTitle, teacherExperience, teacherDirection
            FROM teacher
            WHERE teacherID = %s
        """
    cur.execute(sql, (id,))  # 注意：这里应该是一个元组，即使只有一个元素
    teacher = cur.fetchone()  # 使用 fetchone() 因为您只想获取一个教师记录
    if teacher:
        print(teacher)

        sql = """
            SELECT m.majID, m.majName
            FROM major as m
            JOIN currentassistant as c ON m.majID = c.majID
            JOIN teacher as t ON c.teacherID = t.teacherID
            WHERE t.teacherID = %s
        """
        cur.execute(sql, (id,))
        majorNames = cur.fetchall()
        print(majorNames)

        teacher_majors = [major[1] for major in majorNames]

        teacher_info = TeacherInfo(
            teacherName=teacher[0],
            teacheracademyname=teacher[1],
            teachermajors=teacher_majors,
            teacherTitle=teacher[2],
            teacherExperience=teacher[3],
            teacherDirection=teacher[4]
        )
        return teacher_info

if __name__ == "__main__":
    teacherInfo = getteacherInfo(1)
    if teacherInfo:
        # 在这里处理 teacherInfo 对象
        pass
    else:
        print("No teacher found with ID 1")