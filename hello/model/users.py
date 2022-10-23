# This class is not being used for now.
# Dealing with json


class Users:
    data_store_name = 'users'

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.given_names = [name]
        self.version = '2.0'


class UsersFields:
    USER_ID = 'user_id'
    NAME = 'name'
    GIVEN_NAMES = 'given_names'
