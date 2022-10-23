from cachetools import cached, LRUCache

from hello.db_store.db import MongoDB, DataStores
from hello.const import UsersConsts

# Keeping it global so that it can be updated from add_user
_cache = LRUCache(maxsize=100)


class HelloServiceManager:
    def __init__(self):
        # Get these from configuration.
        db_endpoint = 'mongodb://localhost:27017/'
        db_name = 'hello_db'

        # Should use factory here.
        self._db = MongoDB(db_endpoint, db_name, DataStores.USER_DATA_STORE)

    def get_user_name(self, user_id):
        result = self._get_user_name(user_id)

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
    def _get_user_name(self, user_id):
        query_filter = {UsersConsts.USER_ID: user_id}
        return self._db.get_data(**query_filter)
