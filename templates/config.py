# import pyodbc
import pymssql

# 连接数据库
try:
    conn = pymssql.connect(  # 连接
        host='localhost',  # 服务器主机
        server=r'冰箱\SQLEXPRESS',  # 服务器名
        port='51615',
        database='GraduateAdmissionsSystem',  # 连接的数据库名
        user='sa',  # 访问数据库的用户名
        password='123',  # 密码
        charset='CP936'
    )
    print("Connection successful!")
except pymssql.Error as e:
    print("Error in connection: ", e)  # 连接失败抛出错误原因
    conn = None
    exit(0)  # 退出