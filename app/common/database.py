import os

import pymongo
from pymongo.cursor import Cursor

__author__ = 'richogtz'


class Database(object):
    # URI = "mongodb://richogtz:cloudstrifeFF7!@127.0.0.1:27017"

    URI = os.environ.get('MONGODB_URI') or "mongodb://127.0.0.1:27017/pakke"

    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client.get_database()

    @staticmethod
    def insert(collection, data):
        """

        :param collection:
        :param data:
        :return:
        """
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query, project=None)->Cursor:
        return Database.DATABASE[collection].find(query, project)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)

    @staticmethod
    def aggregate(collection, queries):
        return Database.DATABASE[collection].aggregate(queries)
