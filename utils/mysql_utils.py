import mysql.connector
from os import path, mkdir
from pathlib import Path
import pymysql
import pandas as pd


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


################## Widget 1 ##################
# R10: Use indexing
def getKrc(input_value, input_num):
    with db.cursor() as cursor:
        _checkCol = f"SHOW INDEX FROM academicworld.keyword;"
        cursor.execute(_checkCol)
        result = [r['Key_name'] for r in cursor.fetchall()]
        if 'idx_keyword' not in result:    
            _index = f"CREATE INDEX idx_keyword ON keyword (name);" 
            cursor.execute(_index)
            cursor.fetchall()
        krc = f'SELECT F.name AS name, SUM(PK.score * P.num_citations) AS KRC, F.position as pos, U.name as uni, F.id as id FROM keyword K, publication_keyword PK, faculty F, faculty_publication FP, publication P, university U WHERE PK.keyword_id = K.id AND FP.faculty_id = F.id AND FP.publication_id = P.id AND PK.publication_id = P.id AND F.university_id = U.id AND F.id IN (SELECT K.id FROM keyword K USE INDEX (idx_keyword) WHERE K.name LIKE "%{input_value}%") GROUP BY F.id ORDER BY KRC DESC LIMIT {int(input_num)};'
        cursor.execute(krc)
        result = cursor.fetchall()
        return result

################## Widget 3 ##################
# R11: prepared statements
def getPaper(input_name, input_num):
    with db.cursor() as cursor:
        _prepare = f"PREPARE stmt FROM 'SELECT F.id FROM faculty F WHERE F.name = ? INTO @id';"
        cursor.execute(_prepare)
        _set = f"SET @name='{input_name}';"
        cursor.execute(_set)
        _run = f"EXECUTE stmt USING @name;"
        cursor.execute(_run)
        paper = f'SELECT DISTINCT P.id, P.title AS title, P.year AS year, P.venue AS venue, P.num_citations AS num_citations FROM keyword K, publication_keyword PK, faculty F, faculty_publication FP, publication P WHERE PK.keyword_id = K.id AND FP.faculty_id = F.id AND FP.publication_id = P.id AND PK.publication_id = P.id AND F.id IN (SELECT @id) ORDER BY num_citations DESC LIMIT {int(input_num)};'
        cursor.execute(paper)
        result = cursor.fetchall()
        
        return result    


################## Widget 4 ##################
# R12: create view
def getAllPaper(input_name):
    with db.cursor() as cursor:
        _prepare = f"PREPARE stmt FROM 'SELECT F.id FROM faculty F WHERE F.name = ? INTO @id';"
        cursor.execute(_prepare)
        _set = f"SET @name='{input_name}';"
        cursor.execute(_set)
        _run = f"EXECUTE stmt USING @name;"
        cursor.execute(_run)

        _checkView =f"SHOW FULL TABLES IN academicworld WHERE TABLE_TYPE LIKE '%VIEW%';"
        cursor.execute(_checkView)
        try:
            res = [r['Tables_in_academicworld'] for r in cursor.fetchall()]
            if 'my_view' not in res:
                _view = f"CREATE VIEW my_view AS SELECT DISTINCT P.id AS id, P.title AS title, P.year AS year, P.venue AS venue, P.num_citations AS num_citations, F.id as faculty_id FROM keyword K, publication_keyword PK, faculty F, faculty_publication FP, publication P WHERE PK.keyword_id = K.id AND FP.faculty_id = F.id AND FP.publication_id = P.id AND PK.publication_id = P.id;"
                cursor.execute(_view)
        except Exception as ex:
            _view = f"CREATE VIEW my_view AS SELECT P.id AS id, P.title AS title, P.year AS year, P.venue AS venue, P.num_citations AS num_citations, F.id as faculty_id FROM keyword K, publication_keyword PK, faculty F, faculty_publication FP, publication P WHERE PK.keyword_id = K.id AND FP.faculty_id = F.id AND FP.publication_id = P.id AND PK.publication_id = P.id;"
            cursor.execute(_view)        
        paper = f'SELECT DISTINCT id, title, year, venue, num_citations FROM my_view WHERE faculty_id in (SELECT @id);'    
        cursor.execute(paper)
        result = cursor.fetchall()
        professor = f'SELECT F.name FROM faculty F where F.id in (SELECT @id);'
        cursor.execute(professor)
        professor_name = cursor.fetchall()[0]['name']
        df = pd.DataFrame(result)
        df = pd.pivot_table(df, index=['year'], aggfunc='count')
        return df, professor_name


################## Widget 5 ##################

def getAllKeywords(input_name):
    with db.cursor() as cursor:
        _prepare = f"PREPARE stmt FROM 'SELECT F.id FROM faculty F WHERE F.name = ? INTO @id';"
        cursor.execute(_prepare)
        _set = f"SET @name='{input_name}';"
        cursor.execute(_set)
        _run = f"EXECUTE stmt USING @name;"
        cursor.execute(_run)
        paper = f'SELECT K.id, K.name, COUNT(DISTINCT P.id) FROM keyword K, publication_keyword PK, faculty F, faculty_publication FP, publication P WHERE PK.keyword_id = K.id AND FP.faculty_id = F.id AND FP.publication_id = P.id AND PK.publication_id = P.id AND F.id IN (SELECT @id) GROUP BY K.id;'    
        cursor.execute(paper)
        result = cursor.fetchall()
        professor = f'SELECT F.name FROM faculty F where F.id = (SELECT @id);'
        cursor.execute(professor)
        professor_name = cursor.fetchall()[0]['name']
        df = pd.DataFrame(result).rename(columns={'COUNT(DISTINCT P.id)': 'Publication Number', 'name': 'Keyword'}).sort_values(by='Publication Number', ascending=False)
        return df, professor_name

################## Widget 2 ##################
def likeProfessor(input_name):
    with db.cursor() as cursor:
        _prepare = f"PREPARE stmt FROM 'SELECT F.id FROM faculty F WHERE F.name = ? INTO @id';"
        cursor.execute(_prepare)
        _set = f"SET @name='{input_name}';"
        cursor.execute(_set)
        _run = f"EXECUTE stmt USING @name;"
        cursor.execute(_run)
        _checkCol = f"DESCRIBE faculty;"
        cursor.execute(_checkCol)
        result = [r['Field'] for r in cursor.fetchall()]
        if 'userLike' not in result:
            _addCol = f"ALTER TABLE faculty ADD userLike CHAR(1);"
            cursor.execute(_addCol)
            cursor.fetchall()
        _like = f"UPDATE faculty F SET F.userLike = '1' WHERE F.id IN (SELECT @id);"
        cursor.execute(_like)
        cursor.fetchall()
        _name = f"SELECT F.name FROM faculty F WHERE F.id IN (SELECT @id);"
        cursor.execute(_name)
        _name = cursor.fetchall()
    return _name[0]

def getLiked():
    with db.cursor() as cursor:
        liked = f"SELECT F.id, F.name, U.name FROM faculty F, university U WHERE F.userLike=1 AND U.id = F.university_id;"
        cursor.execute(liked)
        liked = cursor.fetchall()
    return liked

################## Widget 7 ##################

def unlikeProfessor(input_name):
    with db.cursor() as cursor:
        _prepare = f"PREPARE stmt FROM 'SELECT F.id FROM faculty F WHERE F.name = ? INTO @id';"
        cursor.execute(_prepare)
        _set = f"SET @name='{input_name}';"
        cursor.execute(_set)
        _run = f"EXECUTE stmt USING @name;"
        cursor.execute(_run)
        _unlike = f"UPDATE faculty F SET F.userLike = '0' WHERE F.id IN (SELECT @id);"
        cursor.execute(_unlike)
        _unlike = cursor.fetchall()
        _name = f"SELECT F.name FROM faculty F WHERE F.id IN (SELECT @id);"
        cursor.execute(_name)
        _name = cursor.fetchall()
    return _name[0]
                        
if __name__ == '__main__':
    print(getAllPaper('Soloway, Elliot'))