from pymongo import MongoClient


class MongoDBStore:
    def __init__(self, hostname, port):
        self.client = MongoClient(hostname, port)

    def save(self, schemaName, tableName, data):
        """Save the provided data collection to the db"""
        schemaDB = self.client.get_database(schemaName)
        tableDB = schemaDB.get_collection(tableName)
        tableDB.insert_one(data)
