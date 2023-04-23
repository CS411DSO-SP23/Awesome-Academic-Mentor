# LotteZhu

## 0. Title: Awesome Academic Mentor
## 1. Purpose
- Application Scenario: The Awesome Academic Mentor dashboard is a tool designed to help students and researchers to find appropriate academic mentors. The dashboard links to a database of academicworld, which could be used to match students or researchers with mentors who have expertise in their area of interest.
- Target Users: Students and researchers who are looking for academic mentors. These users might be at various stages of their academic careers, from undergraduate students seeking guidance on research projects to Phd candidates searching for dissertation advisors.
- Objectives:   
  - Helping students and researchers find appropriate academic mentors based on their research interests and needs.
  - Providing a user-friendly interface for searching and browsing faculty members, keywords, and publications.
  - Creating a centralized database of academic mentors that could be regularly updated and expanded.
  - Improving the quality and productivity of academic research by connecting students or researchers with experienced mentors who can provide guidance and support.

## 2. Demo
Please check the [demo video]().

## 3. Installation

### 3.1. Package Requirements
```shell
cd /path/to/LotteZhu
pip install -r requirements.txt
```

### 3.2. Database Requirements
- Create a folder `data` under `LotteZhu` 
- Download `faculty.json` and `publications.json` from [MP3 Materials](https://drive.google.com/drive/u/5/folders/1qlR1cvZrQGVN1YnQFx7PUBczaf-PGeCF) into `data/`.
- Download `AcademicWorld.sql` from [MP4 Material](https://drive.google.com/drive/u/5/folders/1NpaunQtKOlDwNXW-ES5XdJdxSnQXI78u) under `data/`.
- Follow the instruction in [MP4 Instructions](https://docs.google.com/document/d/1UKptsVJCnfChfv7QdeZvh1y8FFwatxe5aO6xnp4QbXU/edit) to connect this sql file in mysql
- To create csv files for Neo4j (same as in MP3 Problem 5), run the following command. Then load the csv folder `/path/to/LotteZhu/data/neo4j_data` into Neo4j Desktop as guided in [MP3 Problem 5](https://docs.google.com/document/d/1g5HRJcrkmJz8wOeJsKynB7KUZze6nMC5ng4iYhbnCXA/edit).
```shell
cd /path/to/LotteZhu
python3 utils/neo4j_utils.py
```
- Load the csv files to mongodb
```shell
cd /path/to/LotteZhu
python3 utils/mongodb_utils.py
```
## 4. Usage
### 4.1. Widget I
Widget I helps you find professors who are experts in a specific research area. To use it, just type in the topic you're interested in and choose how many professors you want to see. Then, click the "Search Professors" button to see a list of professors who match your criteria.
### 4.2. Widget II
Widget II lets you search for a professor by their name. Just type in the professor's name and click "Search Profile" to see their information. If you like a professor and want to save their name for future reference, you can click the "Like" button.
### 4.3. Widget III
Widget III helps you find a professor's publications. Just type in the professor's name and choose how many publications you want to see. Then, click the "Show Publications Ordered by Citation Number" button to see a list of the professor's papers, ordered by how many times they have been cited.
### 4.4. Widget IV
Widget IV lets you see how many publications a professor has had over time. To use it, just type in the professor's name and click "Search Publication Time" to see a graph of their publications over time.
### 4.5. Widget V
Widget V helps you see the distribution of research keywords associated with a professor. To use it, just type in the professor's name and choose how many keywords you want to see. Then, click "Search Keyword Distribution" to see a graph of the keywords and how often they appear in the professor's research.
### 4.6. Widget VI
Widget VI lets you see the publication venues (journals, conferences, etc.) where a professor has published their work. To use it, just type in the professor's name and click "Search Publication Venues" to see a list of the venues where the professor has published.
### 4.7. Widget VII
Widget VII lets you manage the professors you've liked in Widget II. To see the professors you've liked, click "Show Liked Professors". To unlike a professor, just type their name in the input field and click "Unlike Professor".

## 5. Design
The application has a single page with seven widgets - details described in section 4 above. 

The application uses several Python libraries, including Dash, plotly, geopandas, and geopy. It also connects to several databases - MongoDB, MySQL, and Neo4j - to retrieve academicworld database.

The code defines a Dash app and loads the necessary databases. The layout is defined with multi-layered Div containing the input, tables, graphs, and charts. Each update function is defined as a callback, triggered by a button click, to update corresponding widge with querying results based on user's inputs.
## 6. Implementation
The implementation of this academic mentor application uses the Dash framework, a Python web application framework that allows for building interactive web applications. The application also uses several Python libraries, including plotly, geopandas, geopy, pymongo, mysql-connector-python, and py2neo.

The application connects to three databases - MongoDB, MySQL, and Neo4j - to retrieve data for the search results and professor profiles. 

The design of the application is based on the Model-View-Controller (MVC) architecture, where the model represents the data and business logic, the view represents the user interface, and the controller handles user input and updates the view accordingly.

The application consists of several callbacks, which are functions that are triggered by user input and update the corresponding widget with querying results. These callbacks use various plotly and Dash components, such as dash_table, dcc.Graph, dcc.Dropdown, dcc.Input, and html.Div, to create the user interface and display the search results and professor profiles.

## 7. Database Techniques: What database techniques have you implemented? How?
### 7.1. Indexing
```python
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
```

The code snippet above implements `indexing` in Widget I, which allows for faster searching of professors based on a research keyword.

The `indexing` technique used here is a non-clustered index on the "name" column of the "keyword" table. The index is created using the SQL command "CREATE INDEX idx_keyword ON keyword (name);". This index allows for faster searching of the "keyword" table based on the "name" column, which is used in the WHERE clause of the query to retrieve professors with a matching keyword.

The function first checks if the index already exists by running the SQL command "SHOW INDEX FROM academicworld.keyword;", which returns a list of all indexes on the "keyword" table. If the index "idx_keyword" does not exist, the function creates the index using the SQL command.

The function then executes a SQL query to retrieve professors with a matching keyword, using the created index. The query uses the "USE INDEX" clause to specify the index to use in the search. This allows for faster search performance than using the default index.

### 7.2. Prepared Statements
```python
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
```
`Prepared statements` is a feature of database management systems that allow SQL statements to be precompiled and optimized for faster execution. The prepared statement is first compiled by the database system and stored in memory. When the statement is executed, only the parameters need to be supplied, and the database system uses the precompiled statement to execute the query.

The code snippet above implements `prepared statements` in Widget III, which allows for faster query execution and improved security against SQL injection attacks. The prepared statement is used to retrieve the ID of the faculty member based on their name. The prepared statement is created using the SQL command "PREPARE stmt FROM 'SELECT F.id FROM faculty F WHERE F.name = ? INTO @id';", which compiles the SELECT statement with a placeholder for the name parameter.

The statement is then executed using the SQL command "EXECUTE stmt USING @name;", which supplies the value of the name parameter using a user-defined variable "@name". This allows for the statement to be executed multiple times with different parameter values, without having to recompile the statement each time.

The function then executes a SQL query to retrieve the publications of the faculty member, using the retrieved ID as a parameter in the WHERE clause of the query.

### 7.3. View
```python
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
```
The code snippet above implements a `View` in Widget IV. A `View` is a virtual table that is created based on the result of a SELECT statement. Views are used to simplify complex queries, provide a consistent view of data, and improve query performance by allowing commonly used queries to be precomputed and stored in memory.

In this code snippet, the `View` is created using the SQL command "CREATE VIEW my_view AS SELECT DISTINCT P.id AS id, P.title AS title, P.year AS year, P.venue AS venue, P.num_citations AS num_citations, F.id as faculty_id FROM keyword K, publication_keyword PK, faculty F, faculty_publication FP, publication P WHERE PK.keyword_id = K.id AND FP.faculty_id = F.id AND FP.publication_id = P.id AND PK.publication_id = P.id;". This creates a View called "my_view" that contains the publication information and faculty ID for all publications in the database.

The function first checks if the `View` already exists by running the SQL command "SHOW FULL TABLES IN academicworld WHERE TABLE_TYPE LIKE '%VIEW%';", which returns a list of all Views in the "academicworld" database. If the View "my_view" does not exist, the function creates the View using the SQL command.

The function then executes a SQL query to retrieve the publications of the faculty member, using the retrieved ID as a parameter in the WHERE clause of the query. The query uses the "my_view" View to retrieve the publication information and filter by the faculty ID of the selected faculty member.


## 8. Extra-Credit Capabilities: What extra-credit capabilities have you developed if any?
Widget VII:
- "Show Liked Professors" button: This button triggers a callback that retrieves the list of liked professors for the current user and displays them in a dash_table.DataTable component.

- "Unlike Professor" button and input field: These components allow the user to remove a professor from their liked list by entering the professor's name in the input field and clicking the "Unlike Professor" button. When the button is clicked, a callback is triggered that change the attribute `likeUser` of the professor from '1' to '0' in the table `faculty`.


## 9. Contributions
- 100% by Lotte Zhu (NetID: lotte88): 24 hours