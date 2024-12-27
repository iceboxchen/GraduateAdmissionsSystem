import pyodbc
import pymssql

# 连接数据库
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\\SQLEXPRESS;'
    'DATABASE=GraduateAdmissionsSystem;'
    'UID=student1;'
    'PWD=tneduts;'  # 之前设置的密码
)

conn = pyodbc.connect(conn_str)