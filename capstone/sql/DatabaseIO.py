import os
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
import pandas as pd

import logging

class DatabaseIO:

    ENV_DB_NAME = 'DB_NAME'
    ENV_DB_SERVER = 'DB_SERVER'
    ENV_DB_USER = 'DB_USER'
    ENV_DB_PWD = 'DB_PWD'

    def __init__(self):
        logging.debug('database_io::__init__')
        #create db connection
        self._conn = connection.MySQLConnection(user = os.getenv(self.ENV_DB_USER), password = os.getenv(self.ENV_DB_PWD),
                                host=os.getenv(self.ENV_DB_SERVER),database=os.getenv(self.ENV_DB_NAME))
        self._cursor = self._conn.cursor()
        
    def __enter__(self):
        return self

    def __exit__(self):
        # close connection
        self._conn.close()

    def commit(self):
        self._conn.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self._conn.close()

    def execute(self, sql, params=None):
        self._cursor.execute(sql, params or ())

    def fetch_all(self):
        return self._cursor.fetchall()

    def fetch_one(self):
        return self._cursor.fetchone()

    def query(self, sql, params=None):
        self._cursor.execute(sql, params or ())
        return self.fetchall()

    def read_to_dataframe(self, sql):
        return pd.read_sql(sql, self._conn)