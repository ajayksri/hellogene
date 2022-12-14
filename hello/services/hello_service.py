from cachetools import cached, LRUCache
from random import randint

from hello.db_store.db import MongoDB, DataStores
from hello.const import UsersConsts

# Keeping it global so that it can be updated from add_user
_cache = LRUCache(maxsize=1000)


class HelloServiceManager:
    def __init__(self, version):
        self._service = None
        if version == 'v1':
            self._service = HelloService()
        else:
            self._service = HelloServiceV2()

    def get_user_name(self, user_id):
        return self._service.get_user_name(user_id)

    def add_user(self, user_id, user_name):
        return self._service.add_user(user_id, user_name)


class HelloService:
    def __init__(self):
        # Get these from configuration.
        db_endpoint = 'mongodb://localhost:27017/'
        db_name = 'hello_db'

        # Should use factory here.
        self._db = MongoDB(db_endpoint, db_name, DataStores.USER_DATA_STORE)

    def get_user_name(self, user_id):
        result = self._get_user_record(user_id)

        if result and UsersConsts.NAME in result:
            return result[UsersConsts.NAME]

        return None

    def add_user(self, user_id, user_name):
        record = {UsersConsts.USER_ID: user_id, UsersConsts.NAME: user_name}
        result = self._db.save_data(record, **{UsersConsts.USER_ID: user_id})
        # Check if it works
        if user_id in _cache:
            _cache.pop(user_id)

        return result

    @cached(cache=_cache)
    def _get_user_record(self, user_id):
        query_filter = {UsersConsts.USER_ID: user_id}
        return self._db.get_data(**query_filter)


class HelloServiceV2(HelloService):
    def __init__(self):
        super().__init__()

    def get_user_name(self, user_id):
        user_record = self._get_user_record(user_id)

        if user_record:
            if UsersConsts.GIVEN_NAMES in user_record and len(user_record[UsersConsts.GIVEN_NAMES]) > 1:
                count = len(user_record[UsersConsts.GIVEN_NAMES])
                index = randint(0, count-1)
                return user_record[UsersConsts.GIVEN_NAMES][index]
            else:
                return user_record[UsersConsts.NAME]

        return None

    def add_user(self, user_id, user_name):
        user_record = self._get_user_record(user_id)
        if user_record is None:
            user_record = {UsersConsts.USER_ID: user_id, UsersConsts.NAME: user_name, UsersConsts.GIVEN_NAMES: [user_name]}
        else:
            if UsersConsts.GIVEN_NAMES in user_record and user_name in user_record[UsersConsts.GIVEN_NAMES]:
                return user_record
            user_record = {UsersConsts.USER_ID: user_id, UsersConsts.GIVEN_NAMES: [user_name]}

        result = self._db.save_data(user_record, **{UsersConsts.USER_ID: user_id})
        # Check if it works
        if user_id in _cache:
            _cache.pop(user_id)

        return result
