from mongo_db_store import MongoDBStore


class DataStoreProvider:
    def __init__(self):
        pass

    def getStore(self, input):
        """Get Store based on the type"""
        if input['type'] == 'database' and input['sub_type'] == 'mongoDB':
            return MongoDBStore(input["ip"], input["port"])
        return None
