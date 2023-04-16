import mysql.connector
from os import path, mkdir
from pathlib import Path
# import pymysql

def loadMySQL():
    curr_path = Path(path.abspath(path.dirname(__file__)))
    proj_path = curr_path.parent
    sql_path = path.join(proj_path, 'data/AcademicWorld.sql')

    db = mysql.connector.connect(
          user='root', 
          password='password',
          host='localhost',
          database='academicworld',
          # max_allowed_packet = '32M'
          )
    
    cursor = db.cursor()
    cursor.execute("SET GLOBAL max_allowed_packet=5073741824")
    with open(sql_path, 'r') as f:
        cursor.execute(f.read(), multi=True)
        # db.commit()
    return db    

if __name__ == '__main__':
    db = loadMySQL()