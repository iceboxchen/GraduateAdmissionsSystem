from flask import Flask, request, render_template, jsonify
import pyodbc

app = Flask(__name__)

# 数据库连接配置
server = 'localhost\\SQLEXPRESS'
database = 'GraduateAdmissionsSystem'
username = 'student1'
password = 'tneduts'


@app.route('/teacher_last_choose')
def teacher_last_choose():
    return render_template('teacher_last_choose.html')


@app.route('/teacher_choosestudent')
def teacher_choosestudent():
    # 连接到数据库
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()

    # 查询教师信息
    query = "SELECT teacherID, year, majID, majName, needstudent FROM teacherqualification WHERE teacherID = '1'"
    cursor.execute(query)

    row = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

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
        conn_str = 'DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=GraduateAdmissionsSystem;UID=student1;PWD=tneduts'
        # 从请求中获取数据
        data = request.get_json()
        teacherID = data['teacherID']
        remainedEnrollment = data['remainedEnrollment']

        # 连接到 SQL Server 数据库
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # 插入数据到 TutorRemainsEnrollment 表
        query = """
        INSERT INTO TutorRemainsEnrollment (teacherID, remainedEnrollment)
        VALUES (?, ?)
        """
        cursor.execute(query, (teacherID, remainedEnrollment))
        conn.commit()

        # 关闭连接
        cursor.close()
        conn.close()

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

        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        cursor = conn.cursor()

        # 查询当前学生是否选择了该教师
        query = """
        SELECT COUNT(*) FROM studentvolunteer
        WHERE studentID = ? AND (volunteerone = ? OR volunteertwo = ? OR volunteerthree = ?)
        """
        cursor.execute(query, (examID, teacherID, teacherID, teacherID))
        result = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

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

        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        cursor = conn.cursor()

        # 查询学生信息
        query = """
        SELECT studentMailBox, studentID, volunteerone, volunteertwo, volunteerthree
        FROM studentvolunteer
        WHERE volunteerone = ? OR volunteertwo = ? OR volunteerthree = ?
        """
        cursor.execute(query, (teacherID, teacherID, teacherID))
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

        conn.close()
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

        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
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

        conn.close()
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

        # 连接到 SQL Server 数据库
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        cursor = conn.cursor()

        # 更新 studentvolunteer 表，将 volunteerfour 设置为当前教师ID，并将 chosennum 设置为 4
        query = """
        UPDATE studentvolunteer
        SET volunteerfour = ?, chosennum = 4
        WHERE studentID = ?
        """
        cursor.execute(query, (teacherID, studentID))
        conn.commit()

        # 关闭连接
        cursor.close()
        conn.close()

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

        # 数据库连接
        conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        cursor = conn.cursor()

        # 更新studentvolunteer表中的chosennum字段
        query = """
        UPDATE studentvolunteer
        SET chosennum = ?
        WHERE studentID = ?
        """
        cursor.execute(query, (chosennum, examID))
        conn.commit()

        # 关闭连接
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": "学生志愿选择更新成功！"})

    except Exception as e:
        print(f"发生错误: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
