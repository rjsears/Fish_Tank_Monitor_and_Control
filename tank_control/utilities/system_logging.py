#!/usr/bin/python3

__author__ = 'Richard J. Sears'
VERSION = "V1.0.0 (2020-06-06)"

##Simple function to read logging config info from MySQL

import sys
sys.path.append('/var/www/fish_tank_control/tank_control/utilities')
import system_info
import mysql.connector
from mysql.connector import Error

def read_logging_config(table, column):
    try:
        connection = mysql.connector.connect(user=system_info.mysql_username,
                                      password=system_info.mysql_password,
                                      host=system_info.mysql_servername,
                                      database=system_info.mysql_database)
        cursor = connection.cursor(buffered=True)
        cursor.execute(("SELECT %s FROM %s") % (column, table))
        for data in cursor:
            database_value = (data[0])
            return database_value
        cursor.close()
        connection.close()
    except Error as error :
        exit()
