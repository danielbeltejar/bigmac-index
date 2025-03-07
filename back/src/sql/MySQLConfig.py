import os


class MySQLConfig(object):

    def __init__(self):
        self._host = os.environ.get('DB_HOST')
        self._port = os.environ.get('DB_PORT')
        self._user = os.environ.get('DB_USER')
        self._password = os.environ.get('DB_PASSWORD')
        self._database = os.environ.get('DB_DATABASE')

    def get_host(self):
        return self._host

    def get_port(self):
        return self._port

    def get_user(self):
        return self._user

    def get_password(self):
        return self._password

    def get_database(self):
        return self._database
