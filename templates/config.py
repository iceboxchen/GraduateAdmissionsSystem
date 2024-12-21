import pyodbc
import pymssql


def iconnect():
    # 连接数据库
    try:
        conn = pymssql.connect(  # 连接
            host='localhost',  # 服务器主机
            server=r'LAPTOP-OL5FK3DD',  # 服务器名
            database='GraduateAdmissionsSystem',  # 连接的数据库名
            user='sa',  # 访问数据库的用户名
            password='123456',  # 密码
        )
        print("Connection successful!")
    except pymssql.Error as e:
        print("Error in connection: ", e)  # 连接失败抛出错误原因
        conn = None
        exit(0)  # 退出

    return conn


conn = iconnect()

# 孙的pyodbc的写法

# conn_str = (
#     'DRIVER={ODBC Driver 17 for SQL Server};'
#     'SERVER=127.0.0.1;'
#     'DATABASE=GraduateAdmissionsSystem;'
#     'UID=sa;'
#     'PWD=sc040717;'  # 之前设置的密码
# )

# conn = pyodbc.connect(conn_str)