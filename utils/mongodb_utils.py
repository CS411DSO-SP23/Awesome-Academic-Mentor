import json
from pymongo import MongoClient

def loadMongoDB():
    # Making Connection
    client = MongoClient("mongodb://localhost:27017/")

    # database
    db = client["academicworld"]

    # Loading or Opening the json file
    with open('./data/faculty.json') as file:
        file_data = json.load(file)

    # Created or Switched to collection
    Collection = db["faculty"]

    # Inserting the loaded data in the Collection
    # if JSON contains data more than one entry
    # insert_many is used else inser_one is used
    if isinstance(file_data, list):
        Collection.insert_many(file_data)
    else:
        Collection.insert_one(file_data)


    with open('./data/publications.json') as file:
        file_data = json.load(file)

    Collection = db["publications"]

    if isinstance(file_data, list):
        Collection.insert_many(file_data)
    else:
        Collection.insert_one(file_data)

    return client    

if __name__ == '__main__':
    db = loadMongoDB()   