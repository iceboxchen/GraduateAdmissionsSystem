bjfu24学年数据库原理及应用课设
1234567团队



--数据库创建
CREATE DATABASE GraduateAdmissionsSystem
ON
(
NAME = GraduateAdmissionsSystem_data,
FILENAME='D:\GraduateAdmissionsSystem\GraduateAdmissionsSystemdata.mdf',
SIZE = 8,
FILEGROWTH = 8
)

LOG ON
(
NAME = GraduateAdmissionsSystem_log,
FILENAME = 'D:\GraduateAdmissionsSystem\GraduateAdmissionsSystemlog.ldf',
SIZE = 8,
FILEGROWTH = 8
);






USE GraduateAdmissionsSystem;

--学院 实体
CREATE TABLE academy(
academyname nchar(20) PRIMARY KEY NOT NULL --学院名称
);
--ALTER TABLE academy
--ADD PRIMARY KEY (academyname);

--一级学科 实体
CREATE TABLE subject(		--一级学科表
	academyname nchar(20) NOT NULL, --学院名称，外键
	subID char(10) PRIMARY KEY NOT NULL,		--学科ID，主键
	subName nvarchar(50) NOT NULL,	--学科名称
    subjectnote nvarchar(255) --备注
);
ALTER TABLE subject
ADD CONSTRAINT FK_subject_academy FOREIGN KEY (academyname) REFERENCES academy(academyname);


--二级学科表 实体
CREATE TABLE major--专业表（二级学科）
(
	majID char(10) NOT NULL,		--二级学科ID，主键
	majName nvarchar(50) NOT NULL,	--二级学科名
	subID char(10) NOT NULL,		--所属学科ID，外键关系 学科表
	majorExamsub nvarchar(50) NOT NULL,	--专业所需考试科目
    majornote nvarchar(255) --备注
    PRIMARY KEY(majID, majName)
);
ALTER TABLE major
ADD CONSTRAINT FK_major_subject FOREIGN KEY (subID) REFERENCES subject(subID);


--教师表 实体
CREATE TABLE teacher		--教师表（导师表）
(
	teacherID char(50) PRIMARY KEY NOT NULL, 	--教师ID，主键
    password char(50) NOT NULL, --教师密码
	teacherName nvarchar(50) NOT NULL, 	--教师姓名
	academyname nchar(20) NOT NULL,		--学院名称
    teacherTitle nvarchar(50) NOT NULL, --教师职称
    teacherExperience nvarchar(255), -- 教师经历
    teacherDirection nvarchar(255) --教师研究方向
);
ALTER TABLE teacher
ADD CONSTRAINT FK_teacher_academy FOREIGN KEY (academyname) REFERENCES academy(academyname);


--教师招生资格表 关系
CREATE TABLE teacherqualification--教师招生资格表（与教师表和当次招生简章表关联）
(
teacherID char(50) NOT NULL,             --教师ID，外键
year int,                                     --学年，主键
majID char(10) NOT NULL,		      --二级学科ID，外键
majName nvarchar(50) NOT NULL,	   --二级学科名
accessfile varbinary, --教师提交的文件（用于审批）
isaccess bit, --是否通过
needstudent int NOT NULL default 0, --教师获得的招生数
PRIMARY KEY (teacherID, year, majID, majName) --教师，学年，二级学科联合主键
);
ALTER TABLE teacherqualification
ADD CONSTRAINT FK_teacherqualification_teacher FOREIGN KEY (teacherID) REFERENCES teacher(teacherID);
ALTER TABLE teacherqualification
ADD CONSTRAINT FK_teacherqualification_major FOREIGN KEY (majID, majName) REFERENCES major(majID, majName);


--招生简章 关系 教师，学科
CREATE TABLE currentassistant --当次招生简章表
(
year int, --学年，外键
majID char(10) NOT NULL,		--二级学科ID，外键
majName nvarchar(50) NOT NULL,	--二级学科名
teacherID char(50) NOT NULL, 	--教师ID，外键
needstudent int CHECK(needstudent > 0),  --招生数，外键
PRIMARY KEY (year, majID, teacherID, majName) --学年，二级学科和教师联合主键
);
ALTER TABLE currentassistant
ADD CONSTRAINT FK_currentassistant_teacherqualification FOREIGN KEY (teacherID, year, majID, majName) REFERENCES teacherqualification(teacherID, year, majID, majName);


--教师招生表
--CREATE TABLE 



CREATE TABLE TutorRemainsEnrollment(	 --仍存在招生指标数的导师
	teacherID char(50) NOT NULL,	  --教师ID，外键
	remainedEnrollment int,	  --剩余招生指标数
	finalEnrollment int	 --最终招生人数
);
ALTER TABLE TutorRemainsEnrollment
ADD CONSTRAINT fk_tutor_teacher FOREIGN KEY (teacherID) REFERENCES teacher(teacherID);


--  成绩表
CREATE TABLE score(
	studentID char(50) PRIMARY KEY NOT NULL,		--准考证号，主键
    year int NOT NULL,
	Firstscore float NOT NULL,  --初试成绩
	Englishscore float(50),  --外语及口语
	Facescore float(50),  --面试成绩
	Majorscore float(50)   --专业成绩
);


-- 教师密码 视图
CREATE VIEW teacherPasswords(Username, Password)
AS SELECT teacherID, password
FROM teacher;


-- 学生密码表（用户）
CREATE TABLE studentPasswords (
    Username char(50) NOT NULL UNIQUE,  -- 用户名，唯一
    Password char(50) NOT NULL,            -- 密码
    
    studentID char(50) PRIMARY KEY NOT NULL,	--准考证号，唯一
	studentName nvarchar(50) NOT NULL, 	--姓名
	studentIDnumber char(50) NOT NULL,   --身份证号
	studentPhone char(50) NOT NULL,       --电话
);


--学生信息表 实体（学生个人信息）
CREATE TABLE studentvolunteer(
    studentID char(50) PRIMARY KEY NOT NULL, --准考证号，唯一
        
    sex nchar(2) CHECK CHECK(sex IN ('男', '女')), --性别
    
    graduatetime char(20), --毕业时间
    
    ResearchInterests
	studentOOS nchar(50),          --生源地
	studentMailBox nchar(50),        --邮箱
	studentUCollege nchar(50),       --本科大学
	studentTypeUCollege nchar(50),  --本科学校类型
	studentUProgram nchar(50),       --本科专业
	studentEContaxt char(50),        --紧急联系人电话
	list varbinary,  --个人简历


    
);
ALTER TABLE studentvolunteer
ADD CONSTRAINT fk_studentvolunteer_studentPasswords FOREIGN KEY (studentID) REFERENCES studentPasswords(studentID);
ALTER TABLE studentvolunteer
ADD CONSTRAINT FK_studentvolunteer_major FOREIGN KEY (majID, majName) REFERENCES major(majID, majName);




--学生志愿表 实体（要填写的表）
CREATE TABLE student_submit_table(
    majID char(10) NOT NULL,		--二级学科ID，外键
    majName nvarchar(50) NOT NULL,	--二级学科名
    studentID char(50) PRIMARY KEY NOT NULL,	--准考证号，唯一
    
    sex nchar(2) CHECK CHECK(sex IN ('男', '女')), --性别
    
    studentUCollege nchar(50),       --本科大学，毕业学校
    studentUTime char(20),     --毕业时间
    studentUProgram nchar(50),       --本科专业
    
	isone bit, --选择应届生
	istwo bit, --选择往届生
    isthree bit, --选择同等学力
    isfour bit, --选择定向生
    isfive bit, --选择非定向生

	studentEContaxt char(50),   --紧急联系人电话
    
    volunteerone char(10), --二级学科下的志愿一教师ID
    volunteertwo char(10), --二级学科下的志愿二教师ID
    volunteerthree char(10), --二级学科下的志愿三教师ID
    
    isReorientation int not null default 0, --是否接受方向调整
    priority1 char(10), --方向1二级学科
    priority2 char(10), --方向2二级学科
    priority3 char(10), --方向3二级学科
    priority4 char(10), --方向4二级学科
    
    nameImage VARBINARY(MAX), --电子签名
    
    volunteerfour char(10), --自由选择的结果：教师ID
    chosennum int CHECK(chosennum IN (0, 1, 2, 3, 4))DEFAULT 0, --0是没有老师选
);
ALTER TABLE student_submit_table
ADD CONSTRAINT fk_student_submit_table_studentPasswords FOREIGN KEY (studentID) REFERENCES studentPasswords(studentID);
ALTER TABLE student_submit_table
ADD CONSTRAINT FK_student_submit_table_major FOREIGN KEY (majID, majName) REFERENCES major(majID, majName);





--管理员 实体
CREATE TABLE admin(
	Username char(50) PRIMARY KEY NOT NULL, 	--管理员ID，主键
    Password char(50) NOT NULL, --管理员密码
)
INSERT INTO admin(Username, Password)
VALUES('admin','admin');





--  测试数据
INSERT INTO academy(academyname)
VALUES ('信息学院');

INSERT INTO subject(academyname,subID,subName,subjectnote)
VALUES    ('信息学院','081200','计算机科学与技术','同等学历加试（01/02/03方向）：科目一：程序设计语言；科目二：离散数学；同等学力加试（04方向）：科目一：计算机图形学；科目二：程序设计语言；同等学力加试（05）：科目一：程序设计语言；科目二：数据库原理。'),
            ('信息学院','085400','电子信息（全日制专业学位）','软件工程(国际联合培养)方向计划招收10人，其余方向共计划招收78人。同等学力加试(01向):科目一:计算机图形学;科目二:程序设计语言。同等学力加试(02/03/04/05方向):科目一:程序设计语言:科目二:离散数学。');

INSERT INTO major(majID, majName, subID, majorExamsub, majornote)
VALUES	('01','大数据技术与人工智能','081200','①应101 思想政治理论②201 英语一③301数学一④408 计算机学科专业基础',''),
		('02','物联网与移动互联网技术','081200','同上',''),
		('04','虚拟现实与计算机视觉','081200','同上',''),
		('01','计算机技术','085400','①101 思想政治理论②204 英语二③302数学二④408 计算机学科专业基础',''),
		('02','软件工程','085400','同上','');        

INSERT INTO teacher(teacherID, password, teacherName, academyname, teacherTitle, teacherExperience, teacherDirection)
VALUES	('1','1','陈诣元','信息学院','教授','毕业于bilibili大学，在文心一言上多次发表文章','致力于用文心一言解决所有作业'),
		('2','2','孙晨','信息学院','副教授','毕业于bjfu','励志实现gpt改变世界'),
        ('3','3','汤世博','信息学院','教授','硕博连读，毕业于我说了你也不知道大学','解决世上一切疑难杂症'),
        ('4','4','曾振宇','信息学院','教授','硕博连读，毕业于皮城大学','用AI让你光活起来');

INSERT INTO teacherqualification(teacherID, year, majID, majName, isaccess, needstudent)
VALUES	('1', '2024', '01', '大数据技术与人工智能', '1', '2'),
		('2', '2024', '01', '计算机技术', '1', '2'),
        ('3', '2024', '02', '物联网与移动互联网技术', '1', '4'),
        ('4', '2024', '02', '软件工程', '1', '4');

INSERT INTO currentassistant(year, majID, majName, teacherID, needstudent)
VALUES	('2024', '01', '大数据技术与人工智能', '1', '2'),
		('2024', '01', '计算机技术', '2', '2'),
        ('2024', '02', '软件工程', '4', '4'),
        ('2024', '02', '物联网与移动互联网技术', '3', '4');






INSERT INTO studentPasswords(Username, Password, studentID, studentName, studentIDnumber, studentPhone)
VALUES	('123', '123','001', '考生1', '000000202411230000','18800001111'),
('456', '456','002', '考生2', '000000202411240000','18800001112'),
('1111', '1111','003', '考生3', '000000202411250000','18800001113'),
('111', '111','004', '考生4', '000000202411260000','18800001114'),
('1212', '1212','005', '考生5', '000000202411270000','18800001115'),
('1234', '1234','006', '考生6', '000000202411280000','18800001116'),
('234', '234','007', '考生7', '000000202411290000','18800001117'),
('345', '345','008', '考生8', '000000202411300000','18800001118'),
('2223', '2223','009', '考生9', '000000202412010000','18800001119'),
('2225', '2225','010', '考生10', '000000202412020000','18800001121');


INSERT INTO studentvolunteer(studentID, studentOOS, studentMailBox, studentUCollege, studentTypeUCollege, studentUProgram, studentEContaxt, majID, majName)
VALUES	('001', '北京', '001@qq.com', '北京林业大学', '211', '物联网工程', '19900001111', '01', '大数据技术与人工智能'),
('002', '南京', '002@qq.com', '北京林业大学', '211', '物联网工程', '19900001112', '01', '大数据技术与人工智能'),
('003', '北京', '003@qq.com', '北京林业大学', '211', '物联网工程', '19900001113', '01', '大数据技术与人工智能'),
('004', '南京', '004@qq.com', '北京林业大学', '211', '物联网工程', '19900001114', '01', '大数据技术与人工智能'),
('005', '北京', '005@qq.com', '北京林业大学', '211', '物联网工程', '19900001115', '01', '大数据技术与人工智能'),
('006', '北京', '006@qq.com', '北京林业大学', '211', '物联网工程', '19900001116', '01', '大数据技术与人工智能'),
('007', '北京', '007@qq.com', '北京林业大学', '211', '物联网工程', '19900001117', '01', '大数据技术与人工智能'),
('008', '北京', '008@qq.com', '北京大学', '985', '物联网工程', '19900001118', '02', '物联网与移动互联网技术');


--孙晨 学生状态表
CREATE TABLE studentState (    
    studentID char(50) PRIMARY KEY NOT NULL,	--准考证号，唯一
	studentName nvarchar(50) NOT NULL, 	--姓名
    state int NoT NULL default 0--学生录取状态
    --0 未完成志愿表
    --1 完成志愿表
    --2 老师选择(时间截止后所有状态是1 的学生变成状态 2)
    --(2->91 录    取)(时间到了所有状态是2的学生自动变成 30)
    --30 双向选择(没有选择学生的老师选择学生)
    --(30->91 录取)(时间到了所有状态是 30 的学生自动变成 31)
    --31 双向选择(有余额的老师和学生双向选择)
    --90 未录取
    --91 被录取
    --时间到了的操作交给管理员
	);

INSERT INTO studentState(studentID, studentName)
VALUES	('001', '考生1'),
('002', '考生2'),
('003', '考生3'),
('004', '考生4'),
('005', '考生5'),
('006', '考生6'),
('007', '考生7'),
('008', '考生8'),
('009', '考生9'),
('010', '考生10');