# LotteZhu
NetID: lotte88

## Title: Awesome Academic Mentor
Purpose: What is the application scenario? Who are the target users? What are the objectives?
Demo: Give the link to your video demo. Read the video demo section below to understand what contents are expected in your demo.
Installation: How to install the application? You don’t need to include instructions on how to install and initially populate the databases if you only use the given dataset.

- Create a folder `data` under `LotteZhu` 
- Download `faculty.json` and `publications.json` from [MP3 Materials](https://drive.google.com/drive/u/5/folders/1qlR1cvZrQGVN1YnQFx7PUBczaf-PGeCF) into `data/`.
- Download `AcademicWorld.sql` from [MP4 Material](https://drive.google.com/drive/u/5/folders/1NpaunQtKOlDwNXW-ES5XdJdxSnQXI78u) under `data/`.

```shell
cd /path/to/LotteZhu
pip install -r requirements.txt
```

- To create csv files for Neo4j (same as in MP3 Problem 5), run the following command. Then load the csv folder `/path/to/LotteZhu/data/neo4j_data` into Neo4j Desktop as guided in [MP3 Problem 5](https://docs.google.com/document/d/1g5HRJcrkmJz8wOeJsKynB7KUZze6nMC5ng4iYhbnCXA/edit).
```shell
cd /path/to/LotteZhu
python3 utils/neo4j_utils.py
```

Usage: How to use it? 
Design: What is the design of the application? Overall architecture and components.
Implementation: How did you implement it? What frameworks and libraries or any tools have you used to realize the dashboard and functionalities?
Database Techniques: What database techniques have you implemented? How?
Extra-Credit Capabilities: What extra-credit capabilities have you developed if any?
Contributions: How each member has contributed, in terms of 1) tasks done and 2) time spent?