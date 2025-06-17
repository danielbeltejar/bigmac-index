from time import sleep

import mysql.connector
from mysql.connector import errorcode

from src.sql.MySQLConfig import MySQLConfig


class MySQL(object):

    def __init__(self):
        self._connect()
        self._create()

    def _connect(self):
        mysql_config = MySQLConfig()
        self._connector = mysql.connector.connect(user=mysql_config.get_user(), password=mysql_config.get_password(),
                                                  host=mysql_config.get_host(),
                                                  port=mysql_config.get_port(),
                                                  database=mysql_config.get_database())

    def _create(self):
        # Open the SQL file and read the contents
        with open('config/table.sql', 'r') as file:
            sql_script = file.read()

        # Create a cursor object
        cursor = self.get_connector().cursor()

        # Execute the SQL commands
        cursor.execute(sql_script)

        # Commit the changes
        self.get_connector().commit()

        # Close the cursor
        cursor.close()

    def get_connector(self):
        while True:
            try:
                # Check if the connection is closed or lost
                if not self._connector.is_connected():
                    self._connect()
                return self._connector
            except mysql.connector.Error as err:
                if err.errno == errorcode.CR_SERVER_LOST or err.errno == errorcode.CR_CONNECTION_ERROR:
                    # Reconnect if the connection was lost or too many connections error occurred
                    sleep(1)
                else:
                    raise
