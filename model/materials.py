from sympy import false

from templates.config import conn

cur = conn.cursor()


def selectsql(sql):
    """输入sql语句，返回搜索结果"""
    cur.execute(sql)
    return cur.fetchall()


def insertsql(text1, text2):
    """
    插入的sql语句
    INSERT INTO text1
    VALUES( text2 )
    """
    sql = " INSERT INTO " + text1 + " VALUES (" + text2 + ")"
    cur.execute(sql)

def insertsql(sql):
    cur.execute(sql)

def updatesql(text1, text2, text3):
    """
    更新的sql语句
    update text1
    set text2
    where text3
    """
    sql = " UPDATE " + text1 + " set " + text2 + " where " + text3
    cur.execute(sql)

def updatesql(sql):
    cur.execute(sql)

class student_submit_data:
    def __init__(self, majID, majName, studentID, sex, studentUCollege, studentUTime,
                 studentUProgram, isone, istwo, isthree, isfour, isfive, studentEContaxt,
                 volunteerone, volunteertwo, volunteerthree, isReorientation, priority1,
                 priority2, priority3, priority4, nameImage):
        self.majID = majID  # 二级学科ID
        self.majName = majName  # 二级学科名
        self.studentID = studentID  # 准考证号
        self.sex = sex  # 性别，只能是男，女
        self.studentUCollege = studentUCollege  # 毕业学校
        self.studentUTime = studentUTime  # 毕业时间，年
        self.studentUProgram = studentUProgram  # 本科专业
        self.isone = isone  # 选择应届生 得到true或false
        self.istwo = istwo  # 选择往届生 得到true或false
        self.isthree = isthree  # 选择同等学力 得到true或false
        self.isfour = isfour  # 选择定向生 得到true或false
        self.isfive = isfive  # 选择非定向生 得到true或false
        self.studentEContaxt = studentEContaxt  # 紧急联系人电话
        self.volunteerone = volunteerone  # 二级学科下的志愿一教师ID
        self.volunteertwo = volunteertwo  # 二级学科下的志愿二教师ID
        self.volunteerthree = volunteerthree  # 二级学科下的志愿三教师ID
        self.isReorientation = isReorientation  # 是否接受方向调整
        self.priority1 = priority1  # 方向1二级学科
        self.priority2 = priority2  # 方向2二级学科
        self.priority3 = priority3  # 方向3二级学科
        self.priority4 = priority4  # 方向4二级学科
        self.nameImage = nameImage  # 电子签名


def getmajorid(majName):
    """根据二级学科名获得二级学科id"""

    pass


def get_checkbox(str):
    """复选框选中则传1，把传过来的转化成数字，没传过来的就是0"""
    if str is None:
        return false
    else:
        return true


def get_teacher_id(teachername, majorname):
    """根据老师ID和所属二级学科获得老师名字
    在同一二级学科下有两个相同名字的老师时失效
    """
    sql = """
    select teacherID
    from currentassistant
    where teacherName = '%s' and year = 2024 and majName = '%s'
    """ % (teachername, majorname)
    result = selectsql(sql)
    if result == []:
        return None
    else:
        return result[0]


def get_teacher_name(teacherid):
    sql = """
    select teacherName
    from teacher
    where teacherID = '%s'
    """ % (teacherid)
    result = selectsql(sql)
    if result == []:
        return None
    else:
        return result[0]


def getallinfo(studentid):
    """通过传进来的准考证号读取所有信息"""
    sql = """
    select majID, majName, studentID, sex, studentUCollege, studentUTime,
        studentUProgram, isone, istwo, isthree, isfour, isfive, studentEContaxt,
        volunteerone, volunteertwo, volunteerthree, isReorientation, priority1,
        priority2, priority3, priority4, nameImage
    from student_submit_table
    join studentPasswords on studentPasswords.studentID = student_submit_table.studentID
    where student_submit_table.studentID = '%s'
    """ % (studentid)
    result = selectsql(sql)
    studentName = result.studentName

    pass


def update_student_submit(studentid,stu_submit_data):
    """通过studentID更新表"""
    sql = """
    select *
    from student_submit_table
    where student_submit_table.studentID = '%s'
    """ % (studentid)
    result = selectsql(sql)
    if result == []:
        sql = """
        INSERT INTO student_submit_table
        values('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s,
        '%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s', %s)
        """ %(stu_submit_data.majID, stu_submit_data.majName, stu_submit_data.studentID,
              stu_submit_data.sex, stu_submit_data.studentUCollege,
              stu_submit_data.studentUTime, stu_submit_data.studentUProgram,
              stu_submit_data.isone, stu_submit_data.istwo, stu_submit_data.isthree,
              stu_submit_data.isfour, stu_submit_data.isfive,
              stu_submit_data.studentEContaxt, stu_submit_data.volunteerone,
              stu_submit_data.volunteertwo, stu_submit_data.volunteerthree,
              stu_submit_data.isReorientation, stu_submit_data.priority1,
              stu_submit_data.priority2, stu_submit_data.priority3,
              stu_submit_data.priority4, (stu_submit_data.nameImage,))
        insertsql(sql)
    else:
        sql = """
        UPDATE stu_submit_data
        SET (majID='%s', majName='%s', sex='%s', studentUCollege='%s',
        studentUTime='%s', studentUProgram='%s', isone=%s, istwo=%s, isthree=%s,
        isfour=%s, isfive=%s, studentEContaxt='%s', volunteerone='%s', volunteertwo='%s',
        volunteerthree='%s', isReorientation=%s, priority1='%s', priority2='%s',
        priority3='%s', priority4='%s', nameImage=%s)
        WHERE stu_submit_data.studentID = '%s'
        """ %(stu_submit_data.majID, stu_submit_data.majName,
              stu_submit_data.sex, stu_submit_data.studentUCollege,
              stu_submit_data.studentUTime, stu_submit_data.studentUProgram,
              stu_submit_data.isone, stu_submit_data.istwo, stu_submit_data.isthree,
              stu_submit_data.isfour, stu_submit_data.isfive,
              stu_submit_data.studentEContaxt, stu_submit_data.volunteerone,
              stu_submit_data.volunteertwo, stu_submit_data.volunteerthree,
              stu_submit_data.isReorientation, stu_submit_data.priority1,
              stu_submit_data.priority2, stu_submit_data.priority3,
              stu_submit_data.priority4, (stu_submit_data.nameImage,)
              , stu_submit_data.studentID)
        updatesql(sql)



def find_teachers(studentID):
    sql="""
    SELECT teacherName
    FROM teacher
    WHERE majID = ( SELECT majID
                    FROM update_student_submit
                    WHERE studentID = '%s')
    """ % (studentID)
