from abc import ABC, abstractmethod
from enum import Enum
from collections import defaultdict

from pymongo import MongoClient


class DBAdmin(ABC):
    def __init__(self, db_endpoint, db_name):
        self._endpoint = db_endpoint
        self._db_name = db_name

    @abstractmethod
    def create_index(self, data_store_name, index_key, **kwargs):
        pass

    @abstractmethod
    def list_indexes(self, data_store_name, **kwargs):
        pass

    @abstractmethod
    def drop_index(self, data_store_name, index_name, **kwargs):
        pass

    @abstractmethod
    def open_connection(self):
        pass

    @abstractmethod
    def close_connection(self):
        pass

    @abstractmethod
    def create_data_store(self, data_store_name, **kwargs):
        pass

    @abstractmethod
    def delete_data_store(self, data_store_name, **kwargs):
        pass

    @abstractmethod
    def get_data_stores(self):
        pass


class DB(ABC):
    def __init__(self, db_endpoint, db_name):
        self._endpoint = db_endpoint
        self._db_name = db_name

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_data(self, **kwargs):
        pass

    @abstractmethod
    def save_data(self, data, **kwargs):
        pass

    @abstractmethod
    def delete_data(self, **kwargs):
        pass


class DBError(Exception):
    pass


class DataStores(Enum):
    USER_DATA_STORE = 'users'


class MongoDBAdmin(DBAdmin):

    def __init__(self, db_endpoint: str, db_name: str, data_store: DataStores) -> None:
        super().__init__(db_endpoint, db_name)
        self._client = self._db = None
        self.open_connection()

    def create_index(self, data_store: DataStores, index_key: str, **kwargs):
        table = self._db[data_store.value]
        response = table.create_index(index_key)

        return response

    def list_indexes(self, data_store_name, **kwargs):
        pass

    def drop_index(self, data_store_name, index_name, **kwargs):
        pass

    def open_connection(self):
        try:
            self._client = MongoClient(self._endpoint)
            self._db = self._client[self._db_name]
        except Exception as e:
            raise DBError(f"Unable to connect data store server endpoints \
                          {self._endpoint} with Error : {e}")
        pass

    def close_connection(self):
        self._client.close()

    def create_data_store(self, data_store: DataStores, **kwargs):
        response = self._db[data_store.value]
        return response

    def delete_data_store(self, data_store: DataStores, **kwargs):
        self._db.drop_collection(data_store.value)

    def get_data_stores(self):
        pass

    def __del__(self):
        self.close_connection()


class MongoDB(DB):
    def __init__(self, db_endpoint: str, db_name: str, data_store: DataStores) -> None:
        super().__init__(db_endpoint, db_name)
        self._data_store_name = data_store.value
        self._client = self._data_store = None
        self.open()

    def open(self):
        try:
            self._client = MongoClient(self._endpoint)
            db = self._client[self._db_name]
            self._data_store = db[self._data_store_name]
        except Exception as e:
            raise DBError(f"Unable to connect data store server endpoints \
                          {self._endpoint} with Error : {e}")

    def get_data(self, **kwargs):
        query_filter = kwargs
        return self._data_store.find_one(query_filter)

    def save_data(self, data, **kwargs):
        try:
            query_filter = kwargs
            updates = defaultdict(dict)
            for a_key in data:
                if isinstance(data[a_key], list):
                    updates['$push'][a_key] = data[a_key]
                else:
                    updates['$set'][a_key] = data[a_key]

            self._data_store.find_one_and_update(query_filter, updates, upsert=True)
        except Exception as e:
            raise DBError(f"Unable to save data to data store. Error {e}")

    def delete_data(self, **kwargs):
        pass

    def close(self):
        self._client.close()

    def __del__(self):
        self.close()
