import pandas as pd
from pandas import json_normalize
import json
from tqdm import tqdm
from neo4j import GraphDatabase
from os import path, mkdir
from pathlib import Path
# from data_utils import createDataset   
from utils.data_utils import createDataset  

def processCSV():
    curr_path = Path(path.abspath(path.dirname(__file__)))
    proj_path = curr_path.parent
    json_path = path.join(proj_path, 'data')
    csv_path = path.join(json_path, 'neo4j_data')

    print('Post processing to faculty.csv')
    faculty_entity:pd.DataFrame = pd.read_csv(path.join(csv_path, 'faculty.csv'))
    faculty_entity[':LABEL'] = 'FACULTY'
    faculty_entity['id'] = faculty_entity.apply(lambda x: 'f%d' % x['id'], axis=1)
    faculty_entity.rename(columns={'id' : 'id:ID'}, inplace=True)
    faculty_entity.to_csv(path.join(csv_path, 'faculty.csv'), index=False)

    print('Post processing to institute.csv')
    institute_entity:pd.DataFrame = pd.read_csv(path.join(csv_path, 'institute.csv'))
    institute_entity[':LABEL'] = 'INSTITUTE'
    institute_entity['id'] = institute_entity.apply(lambda x: 'i%d' % x['id'], axis=1)
    institute_entity.rename(columns={'id' : 'id:ID'}, inplace=True)
    institute_entity.to_csv(path.join(csv_path, 'institute.csv'), index=False)

    print('Post processing to keyword.csv')
    keyword_entity:pd.DataFrame = pd.read_csv(path.join(csv_path, 'keyword.csv'))
    keyword_entity[':LABEL'] = 'KEYWORD'
    keyword_entity['id'] = keyword_entity.apply(lambda x: 'k%d' % x['id'], axis=1)
    keyword_entity.rename(columns={'id' : 'id:ID'}, inplace=True)
    keyword_entity.to_csv(path.join(csv_path, 'keyword.csv'), index=False)

    print('Post processing to publication.csv')
    publication_entity:pd.DataFrame = pd.read_csv(path.join(csv_path, 'publication.csv'))
    publication_entity['id'] = publication_entity.apply(lambda x: 'p%d' % x['id'], axis=1)
    publication_entity[':LABEL'] = 'PUBLICATION'
    publication_entity['title'] = publication_entity.apply(lambda x: x['title'].strip(), axis=1)
    publication_entity['venue'] = publication_entity.apply(lambda x: ' '.join(str(x['venue']).split()) if x['venue'] else '', axis=1)
    publication_entity.rename(columns={'id' : 'id:ID', 'year' : 'year:long', 'numCitations' : 'numCitations:long'}, inplace=True)
    publication_entity.to_csv(path.join(csv_path, 'publication.csv'), index=False)

    print('Post processing to faculty_affiliation.csv')
    faculty_affiliation:pd.DataFrame = pd.read_csv(path.join(csv_path, 'faculty_affiliation.csv'))
    faculty_affiliation[':TYPE'] = 'AFFILIATION_WITH'
    faculty_affiliation['id'] = faculty_affiliation.apply(lambda x: 'f%d' % x['id'], axis=1)
    faculty_affiliation['affiliation.id'] = faculty_affiliation.apply(lambda x: 'i%d' % x['affiliation.id'], axis=1)
    faculty_affiliation.rename(columns={'id' : ':START_ID', 'affiliation.id' : ':END_ID'}, inplace=True)
    faculty_affiliation.to_csv(path.join(csv_path, 'faculty_affiliation.csv'), index=False)

    print('Post processing to faculty_keyword.csv')
    faculty_keyword:pd.DataFrame = pd.read_csv(path.join(csv_path, 'faculty_keyword.csv'))
    faculty_keyword[':TYPE'] = 'INTERESTED_IN'
    faculty_keyword['id'] = faculty_keyword.apply(lambda x: 'f%d' % x['id'], axis=1)
    faculty_keyword['keywords.id'] = faculty_keyword.apply(lambda x: 'k%d' % x['keywords.id'], axis=1)
    faculty_keyword.rename(columns={'id' : ':START_ID', 'keywords.id' : ':END_ID', 'keywords.score' : 'score:float'}, inplace=True)
    faculty_keyword.to_csv(path.join(csv_path, 'faculty_keyword.csv'), index=False)

    print('Post processing to faculty_publication.csv')
    faculty_publication:pd.DataFrame = pd.read_csv(path.join(csv_path, 'faculty_publication.csv'))
    faculty_publication[':TYPE'] = 'PUBLISH'
    faculty_publication['id'] = faculty_publication.apply(lambda x: 'f%d' % x['id'], axis=1)
    faculty_publication['publications'] = faculty_publication.apply(lambda x: 'p%d' % x['publications'], axis=1)
    faculty_publication.rename(columns={'id' : ':START_ID', 'publications' : ':END_ID'}, inplace=True)
    faculty_publication.to_csv(path.join(csv_path, 'faculty_publication.csv'), index=False)

    print('Post processing to publication_keyword.csv')
    publication_keyword:pd.DataFrame = pd.read_csv(path.join(csv_path, 'publication_keyword.csv'))
    publication_keyword[':TYPE'] = 'LABEL_BY'
    publication_keyword['id'] = publication_keyword.apply(lambda x: 'p%d' % x['id'], axis=1)
    publication_keyword['keywords.id'] = publication_keyword.apply(lambda x: 'k%d' % x['keywords.id'], axis=1)
    publication_keyword.rename(columns={'id' : ':START_ID', 'keywords.id' : ':END_ID', 'keywords.score' : 'score:float'}, inplace=True)
    publication_keyword.to_csv(path.join(csv_path, 'publication_keyword.csv'), index=False)



def generateNEO4JCSV():
    curr_path = Path(path.abspath(path.dirname(__file__)))
    proj_path = curr_path.parent
    json_path = path.join(proj_path, 'data')
    csv_path = path.join(json_path, 'neo4j_data')
    if not path.exists(csv_path):
        mkdir(csv_path)

    createDataset([
        path.join(json_path, 'faculty.json'), 
        path.join(csv_path, 'faculty.csv'), 
        'id, name, position, researchInterest, email, phone, photoUrl'
        ])
    
    createDataset([
        path.join(json_path, 'faculty.json'), 
        path.join(csv_path, 'institute.csv'), 
        'affiliation.id, affiliation.name, affiliation.photoUrl',
        'id, name, photoUrl'
        ])
    
    createDataset([
        path.join(json_path, 'publications.json'), 
        path.join(csv_path, 'keyword.csv'), 
        'keywords.id, keywords.name',
        'id, name',
        ])
    
    createDataset([
        path.join(json_path, 'publications.json'), 
        path.join(csv_path, 'publication.csv'), 
        'id, title, venue, year, numCitations',
    ])

    createDataset([
        path.join(json_path, 'publications.json'), 
        path.join(csv_path, 'publication_keyword.csv'), 
        'id, keywords.id, keywords.score',
    ])

    createDataset([
        path.join(json_path, 'faculty.json'),
        path.join(csv_path, 'faculty_affiliation.csv'), 
        'id, affiliation.id',
    ])

    createDataset([
        path.join(json_path, 'faculty.json'),
        path.join(csv_path, 'faculty_keyword.csv'),
        'id, keywords.id, keywords.score',
    ])

    createDataset([
        path.join(json_path, 'faculty.json'),
        path.join(csv_path, 'faculty_publication.csv'), 
        'id, publications',
    ])

    processCSV()

################## Widget 6 ##################

def getVenues(input_name):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    with driver.session(database='academicworld') as session:
        result = session.run(f"MATCH (f:FACULTY)-[:PUBLISH]->(pub:PUBLICATION) WHERE f.name='{input_name}' RETURN pub.venue" )
        res = []
        for r in result:
            res.append(r.data())
        return pd.DataFrame(res)

if __name__ == '__main__':
    generateNEO4JCSV()
