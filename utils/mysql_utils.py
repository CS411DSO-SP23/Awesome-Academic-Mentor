import mysql.connector
from os import path, mkdir
from pathlib import Path
import pymysql


curr_path = Path(path.abspath(path.dirname(__file__)))
proj_path = curr_path.parent
sql_path = path.join(proj_path, 'data/AcademicWorld.sql')

# db = mysql.connector.connect(
db = pymysql.connect(
        user='root', 
        password='password',
        host='127.0.0.1',
        database='academicworld',
        charset='utf8mb4',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
        # max_allowed_packet = '32M'
        )

# cursor = db.cursor()
# cursor.execute("SET GLOBAL max_allowed_packet=5073741824")
# with open(sql_path, 'r') as f:
#     cursor.execute(f.read(), multi=True)
#     # db.commit() 

def getKrc(input_value):
    with db.cursor() as cursor:
        krc = f'SELECT F.name AS name, SUM(PK.score * P.num_citations) AS KRC, F.position as pos, U.name as uni, F.id as id FROM keyword K, publication_keyword PK, faculty F, faculty_publication FP, publication P, university U WHERE K.name = "{input_value}" and PK.keyword_id = K.id AND FP.faculty_id = F.id AND FP.publication_id = P.id AND PK.publication_id = P.id AND F.university_id = U.id GROUP BY F.id ORDER BY KRC DESC LIMIT 10;'
        cursor.execute(krc)
        result = cursor.fetchall()
        return result
    
def getPaper(professor_id):
    with db.cursor() as cursor:
        paper = f'SELECT P.title, P.year, P.venue, P.num_citations FROM keyword K, publication_keyword PK, faculty F, faculty_publication FP, publication P WHERE F.id = "{professor_id}" AND PK.keyword_id = K.id AND FP.faculty_id = F.id AND FP.publication_id = P.id AND PK.publication_id = P.id GROUP BY F.id ORDER BY KRC DESC LIMIT 10;'
        cursor.execute(paper)
        result = cursor.fetchall()
        return result    

if __name__ == '__main__':
    print(getKrc('machine learning'))