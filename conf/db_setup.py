import sys

from pymongo import MongoClient
from hello.db_store.db import DataStores


def setup_db(db_name):
    db_client = MongoClient('mongodb://localhost:27017/')
    db_instance = db_client[db_name]
    data_stores = list(map(lambda ds: ds.value, DataStores))
    user_collection = db_instance[data_stores[0]]  # There is only one data store right now.

    # create index
    try:
        response = user_collection.create_index('user_id')
        print(response)
    except Exception as ex:
        print(ex)

    # Insert a record to see if db is configured properly.
    user_record = {"user_id": "ajay123", "name": "Ajay"}
    response = user_collection.insert_one(user_record)
    print(response.inserted_id)

    # Check if record is there
    find_query = {"user_id": "ajay123"}
    num_records = user_collection.count_documents(find_query)
    if num_records == 0:
        print("Error: Database is not configured properly.")
        sys.exit(1)

    # Delete the record
    del_query = {"user_id": "ajay123"}
    response = user_collection.delete_one(del_query)
    print(response)


def cleanup_db(db_name):
    db_client = MongoClient('mongodb://localhost:27017/')
    db_client.drop_database(db_name)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        setup_db('hello_db')  # Fixed dbname, should be picked from config file.
    elif len(sys.argv) == 2 and sys.argv[1] == '--clean':
        cleanup_db('hello_db')
    else:
        print("Error: Usage: python3 db_setup.py [--clean]")
