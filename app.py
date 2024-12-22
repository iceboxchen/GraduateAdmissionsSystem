from exceptiongroup import catch
from flask import Flask, render_template
from flask import redirect
from flask import url_for
from flask import request
from sympy.codegen.ast import continue_

from model.check_login import is_existed_student, exist_user_student, is_null, is_existed_teacher, exist_user_teacher, is_existed_admin, exist_user_admin
from model.check_regist import add_user
from model.admin_submit import is_null_submit, admin_submit
from model.getCurrentassistantData import getMajorNote, getSubjectNote, getNeedStudent, getSubject, getMajor
from model.getstudentState import getstudentState, getstudentState
from model.getteacherInfo import getteacherInfo
from model import materials

app = Flask(__name__)


@app.route('/')
def index():
    # pass
    return render_template('identify_choose.html')


@app.route('/admin')
def admin():
    return render_template('admin_login.html')


@app.route('/admin2_login', methods=['GET', 'POST'])
def admin2_login():
    if request.method == 'POST':  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('admin_login.html', message=login_massage)
        elif is_existed_admin(username, password):
            return render_template('admin_index.html', username=username)
        elif exist_user_admin(username):
            login_massage = "温馨提示：密码错误，请输入正确密码"
            return render_template('admin_login.html', message=login_massage)
        else:
            login_massage = "温馨提示：不存在该用户，请先注册"
            return render_template('admin_login.html', message=login_massage)
    return render_template('student_login.html')


@app.route("/submit_scores", methods=["GET", 'POST'])
def submit_scores():
    if request.method == 'POST':
        studentID = request.form['studentID']
        year = request.form['year']
        Firstscore = request.form['Firstscore']
        Englishscore = request.form['Englishscore']
        Facescore = request.form['Facescore']
        Majorscore = request.form['Majorscore']
        if is_null_submit(studentID, year, Firstscore, Englishscore, Facescore, Majorscore):
            login_massage = "温馨提示：都是是必填项"
            return render_template('admin_index.html', message=login_massage)
        else:
            admin_submit(request.form['studentID'], request.form['year'], request.form['Firstscore'], request.form['Englishscore'], request.form['Facescore'], request.form['Majorscore'])
            return render_template('submit_success.html')
    return render_template('admin_index.html')


@app.route('/teacher_login')
def teacher_login():
    return render_template('teacher_login.html')


@app.route('/teacher2_login', methods=['GET', 'POST'])
def teacher2_login():
    if request.method == 'POST':  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('teacher_login.html', message=login_massage)
        elif is_existed_teacher(username, password):
            teacher_info = getteacherInfo(username)
            return render_template('teacher_index.html', teacher_info=teacher_info)
        elif exist_user_teacher(username):
            login_massage = "温馨提示：密码错误，请输入正确密码"
            return render_template('teacher_login.html', message=login_massage)
        else:
            login_massage = "温馨提示：不存在该用户，请先注册"
            return render_template('teacher_login.html', message=login_massage)
    return render_template('teacher_login.html')


@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    return render_template('student_login.html')


@app.route('/student2_login', methods=['GET', 'POST'])
def student2_login():
    if request.method == 'POST':  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('student_login.html', message=login_massage)
        if is_existed_student(username, password):
            # 假设用户名即为学生ID
            student_State = getstudentState(username)
            print(student_State)
            if student_State is not None:
                return render_template('student_index.html', student_State=student_State)
            else:
                login_message = "温馨提示：无法获取学生状态"
                return render_template('student_login.html', message=login_message)
        elif exist_user_student(username):
            login_massage = "温馨提示：密码错误，请输入正确密码"
            return render_template('student_login.html', message=login_massage)
        else:
            login_massage = "温馨提示：不存在该用户，请先注册"
            return render_template('student_login.html', message=login_massage)
    return render_template('student_login.html')


@app.route('/student_index', methods=['GET', 'POST'])
def student_index():
    return render_template('student_index.html')


@app.route('/student_submit', methods=['GET', 'POST'])
def student_submit():
    return render_template('student_submit.html')


@app.route("/register", methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        studentID = request.form['studentID']  # 获取准考证号
        studentName = request.form['studentName']  # 获取姓名
        studentIDnumber = request.form['studentIDnumber']  # 获取身份证号
        studentPhone = request.form['studentPhone']  # 获取电话号码
        if is_null(username, password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('student_register.html', message=login_massage)
        elif exist_user_student(username):
            login_massage = "温馨提示：用户已存在，请直接登录"
            return render_template('student_register.html', message=login_massage)
        else:
            add_user(request.form['username'], request.form['password'], request.form['studentID'], request.form['studentName'], request.form['studentIDnumber'], request.form['studentPhone'])
            return render_template('student_index.html', username=username)
    return render_template('student_register.html')


# 招生简章
@app.route('/currentassistant')
def currentassistant():
    subjects = getSubject()
    majors = getMajor()
    needstudents = getNeedStudent()
    subjectnotes = getSubjectNote()
    majornotes = getMajorNote()

    # 重组数据
    currentassistant_info = {
        'subjects': subjects,
        'majors': majors,
        'needstudents': needstudents,
        'subjectnotes': subjectnotes,
        'majornotes': majornotes
    }

    # 打印重组后的数据（通常用于调试）
    print(currentassistant_info)

    # 渲染模板并传递数据
    return render_template('currentassistant.html', currentassistant=currentassistant_info)


# 上传学生表
@app.route("/student2_submit", methods=['GET', 'POST'])
def student2_submit():
    submit_message = ""
    # 先识别上传的人的身份然后再上传对应的内容
    if request.method == 'POST':
        majName = request.form['major']  # 复试学科
        stusex = request.form['gender']  # 学生性别

        def getnum(str):
            temp = None
            try:
                temp = request.form[str]
            except:
                print("发生异常")
            return materials.get_checkbox(temp)

        isone = getnum('fresh-graduate') # 选择应届生
        istwo = getnum('previous-graduate') #选择往届生
        isthree = getnum('equal-education') #选择同等学力
        isfour = getnum('targeted-student') #选择定向生
        isfive = getnum('non-targeted-student') #选择非定向生

        if request.form['save'] == "提交":
            if (isone and istwo and isthree) or (isone and istwo) or (istwo and isthree) or (isthree and isone):
                return render_template('student_submit.html', message="应届生、往届生、同等学力必须三选一", heat="")
            elif (isfour and isfive) or (not isfour and not isfive):
                return render_template('student_submit.html', message="请正确选择定向生和非定向生")

        studentUCollege = request.form['graduation-school']  # 本科大学
        studentUTime = request.form['graduation-time']  # 毕业时间
        studentUMajor = request.form['major-study'] # 毕业专业

        # password = request.form['contact-phone'] # 考生联系方式不改
        studentEContaxt = request.form['emergency-contact'] # 紧急联系人手机

        volunteerone = request.form['advisor-preference1'] # 志愿一教师名
        volunteertwo = request.form['advisor-preference2'] # 志愿二教师名
        volunteerthree = request.form['advisor-preference3'] # 志愿三教师名

        volunteerone = materials.get_teacher_id(volunteerone, majName)
        volunteertwo = materials.get_teacher_id(volunteertwo, majName)
        volunteerthree = materials.get_teacher_id(volunteerthree, majName)

        ResearchInterests = request.form['research-direction']  # 拟报研究方向

        isReorientation = request.form['adjustment']  # 是否接受方向调整，即选择该一级学科下的其他二级学科
        priority1 = request.form['priority1'] # 二级学科1只参与双向选择
        priority2 = request.form['priority2'] # 二级学科2只参与双向选择
        priority3 = request.form['priority3'] # 二级学科3只参与双向选择
        priority4 = request.form['priority4'] # 二级学科4只参与双向选择

        nameImage = request.form['signatureUpload'] # 考生签名（图片）

        materials.update_student_submit()

        # else:
        #     add_user(request.form['username'], request.form['password'], request.form['studentID'],
        #              request.form['studentName'], request.form['studentIDnumber'], request.form['studentPhone'])
        #     return render_template('student_submit.html', username=username)
    allinfo = materials.getallinfo()
    return render_template('student_submit.html', message = submit_message, info = allinfo)


@app.route('/teacher_last_choose')
def teacher_last_choose():
    return render_template('teacher_last_choose.html')


@app.route('/teacher_choosestudent')
def teacher_choosestudent():
    # 连接到数据库
    cursor = conn.cursor()

    # 查询教师信息
    query = "SELECT teacherID, year, majID, majName, needstudent FROM teacherqualification WHERE teacherID = '1'"
    cursor.execute(query)

    row = cursor.fetchone()

    # 关闭数据库连接


    # 如果查询到教师信息，则传递到模板
    if row:
        teacherID = row[0]
        year = row[1]
        majID = row[2]
        majName = row[3]
        needstudent = row[4]
    else:
        teacherID = year = majID = majName = needstudent = "未知"

    return render_template('teacher_choosestudent.html', teacherID=teacherID, year=year, majID=majID, majName=majName,
                           needstudent=needstudent)


@app.route('/save_remained_enrollment', methods=['POST'])
def save_remained_enrollment():
    try:
        # 从请求中获取数据
        data = request.get_json()
        teacherID = data['teacherID']
        remainedEnrollment = data['remainedEnrollment']

        # 连接到 SQL Server 数据库

        cursor = conn.cursor()

        # 插入数据到 TutorRemainsEnrollment 表
        query = """
        INSERT INTO TutorRemainsEnrollment (teacherID, remainedEnrollment)
        VALUES ('%s', '%s')
        """% (teacherID, remainedEnrollment)
        cursor.execute(query)
        conn.commit()

        # 关闭连接
        cursor.close()

        # 返回成功响应
        return jsonify({"success": True})

    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/update_student_status', methods=['POST'])
def update_student_status():
    try:
        data = request.get_json()

        teacherID = data['teacherID']
        examID = data['examID']

        cursor = conn.cursor()

        # 查询当前学生是否选择了该教师
        query = """
        SELECT COUNT(*) FROM studentvolunteer
        WHERE studentID = '%s' AND (volunteerone = '%s' OR volunteertwo = '%s' OR volunteerthree = '%s')
        """% (examID, teacherID, teacherID, teacherID)
        cursor.execute(query)
        result = cursor.fetchone()

        conn.commit()

        cursor.close()

        return jsonify({"success": True})

    except Exception as e:
        print(f"数据库连接或查询失败: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/get_student_volunteer_info', methods=['GET'])
def get_student_volunteer_info():
    try:
        teacherID = request.args.get('teacherID').strip()
        if not teacherID:
            return jsonify({"error": "teacherID is required"}), 400

        cursor = conn.cursor()

        # 查询学生信息
        query = """
        SELECT studentMailBox, studentID, volunteerone, volunteertwo, volunteerthree
        FROM studentvolunteer
        WHERE volunteerone = '%s' OR volunteertwo = '%s' OR volunteerthree = '%s'
        """% (teacherID, teacherID, teacherID)
        cursor.execute(query)
        rows = cursor.fetchall()

        student_data = {
            "volunteerone": [],
            "volunteertwo": [],
            "volunteerthree": []
        }

        for row in rows:
            student = {
                "name": row[0].strip(),
                "examID": row[1].strip()
            }
            if row[2].strip() == teacherID:
                student_data["volunteerone"].append(student)
            if row[3].strip() == teacherID:
                student_data["volunteertwo"].append(student)
            if row[4].strip() == teacherID:
                student_data["volunteerthree"].append(student)


        return jsonify(student_data)

    except Exception as e:
        print(f"数据库连接或查询失败: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/get_pending_students_info', methods=['GET'])
def get_pending_students_info():
    try:
        teacherID = request.args.get('teacherID').strip()
        if not teacherID:
            return jsonify({"error": "teacherID is required"}), 400

        cursor = conn.cursor()

        # 查询 chosennum 为 0 的学生信息
        query = """
        SELECT studentID
        FROM studentvolunteer
        WHERE chosennum = 0
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        students = []
        for row in rows:
            student = {
                "examID": row[0].strip(),
            }
            students.append(student)


        return jsonify({"students": students})

    except Exception as e:
        print(f"数据库连接或查询失败: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/admit_student', methods=['POST'])
def admit_student():
    try:
        # 从请求中获取数据
        data = request.get_json()
        teacherID = data['teacherID']
        studentID = data['studentID']

        cursor = conn.cursor()

        # 更新 studentvolunteer 表，将 volunteerfour 设置为当前教师ID，并将 chosennum 设置为 4
        query = """
        UPDATE studentvolunteer
        SET volunteerfour = '%s', chosennum = 4
        WHERE studentID = '%s'
        """% (teacherID, studentID)
        cursor.execute(query)
        conn.commit()

        # 关闭连接
        cursor.close()

        # 返回成功响应
        return jsonify({"success": True})

    except Exception as e:
        print(f"数据库连接或查询失败: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/update_student_volunteer_choice', methods=['POST'])
def update_student_volunteer_choice():
    try:
        # 获取前端传来的数据
        data = request.get_json()
        examID = data['examID']  # 学生的examID
        chosennum = data['chosennum']  # 志愿顺序 1-第一志愿，2-第二志愿，3-第三志愿

        # 校验chosennum的值，确保是合法的
        if chosennum not in [1, 2, 3]:
            return jsonify({"success": False, "message": "chosennum值无效，应为1、2或3。"}), 400

        cursor = conn.cursor()

        # 更新studentvolunteer表中的chosennum字段
        query = """
        UPDATE studentvolunteer
        SET chosennum = '%s'
        WHERE studentID = '%s'
        """% (chosennum, examID)
        cursor.execute(query)
        conn.commit()

        # 关闭连接
        cursor.close()

        return jsonify({"success": True, "message": "学生志愿选择更新成功！"})

    except Exception as e:
        print(f"发生错误: {e}")
        return jsonify({"success": False, "message": str(e)}), 500



if __name__ == "__main__":
    app.run()



