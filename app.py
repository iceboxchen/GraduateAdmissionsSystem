from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request
from model.check_login import is_existed_student, exist_user_student, is_null, is_existed_teacher, exist_user_teacher, is_existed_admin, exist_user_admin
from model.check_regist import add_user
from model.admin_submit import is_null_submit,admin_submit
from model.getCurrentassistantData import getMajorNote, getSubjectNote, getNeedStudent, getSubject, getMajor
from model.getstudentState import getstudentState, getstudentState
from model.getteacherInfo import getteacherInfo

app = Flask(__name__)

@app.route('/')
def index():
    # pass
    return render_template('identify_choose.html')

@app.route('/admin')
def admin():
    return render_template('admin_login.html')
@app.route('/admin2_login',methods=['GET','POST'])
def admin2_login():
    if request.method=='POST':  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        if is_null(username,password):
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
@app.route("/submit_scores",methods=["GET", 'POST'])
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
@app.route('/teacher2_login',methods=['GET','POST'])
def teacher2_login():
    if request.method=='POST':  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        if is_null(username,password):
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

@app.route('/student_login',methods=['GET','POST'])
def student_login():
    return render_template('student_login.html')
@app.route('/student2_login',methods=['GET','POST'])
def student2_login():
    if request.method=='POST':  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        if is_null(username,password):
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


@app.route('/student_index',methods=['GET','POST'])
def student_index():
    return render_template('student_index.html')

@app.route('/student_submit',methods=['GET','POST'])
def student_submit():
    return render_template('student_submit.html')

@app.route("/register",methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        studentID = request.form['studentID']  # 获取准考证号
        studentName = request.form['studentName']  # 获取姓名
        studentIDnumber = request.form['studentIDnumber']  # 获取身份证号
        studentPhone = request.form['studentPhone']  # 获取电话号码
        if is_null(username,password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('student_register.html', message=login_massage)
        elif exist_user_student(username):
            login_massage = "温馨提示：用户已存在，请直接登录"
            return render_template('student_register.html', message=login_massage)
        else:
            add_user(request.form['username'], request.form['password'],request.form['studentID'] , request.form['studentName'],request.form['studentIDnumber'] ,request.form['studentPhone'])
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


if __name__=="__main__":
    app.run()


