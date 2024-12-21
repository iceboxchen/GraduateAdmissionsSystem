import pyodbc
import pymssql

# 连接数据库
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=127.0.0.1;'
    'DATABASE=GraduateAdmissionsSystem;'
    'UID=sa;'
    'PWD=sc040717;'  # 之前设置的密码
)

conn = pyodbc.connect(conn_str)