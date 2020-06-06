#!/usr/bin/python3

'''
use_database.py is a system wide database module designed to be called by any other module
that needs to use either the mysql database or the influx database.
'''

__author__ = 'Richard J. Sears'
VERSION = "V1.0 (2020-06-06)"

import system_info
import mysql.connector
from mysql.connector import Error
from influxdb import InfluxDBClient, exceptions
from system_logging import read_logging_config
import logging

# Setup module Logging. Main setup is done in tank_control_master.py
level = read_logging_config('logging', 'log_level')
level = logging._checkLevel(level)
log = logging.getLogger(__name__)
log.setLevel(level)


def read_mysql_database(table, column):
    log.debug( f'read_mysql_database() called with ({table}, {column})')
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
        log.warning("Failed to read record from database: {}".format(error))
        exit()

def update_mysql_database(table,column,value):
    log.debug(f'update_mysql_database() called with Table: {table}, Column: {column}, Value: {value}')
    try:
        connection = mysql.connector.connect(user=system_info.mysql_username,
                                      password=system_info.mysql_password,
                                      host=system_info.mysql_servername,
                                      database=system_info.mysql_database)
        cursor = connection.cursor(buffered=True)
        sql_update = "UPDATE " + table + " SET " + column + " = %s"
        cursor.execute(sql_update, (value,))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as error :
        log.warning(f'Failed to Update record in database: {error}')
        exit()


def insert_mysql_database(table,column,value):
    log.debug(f'insert_mysql_database() called with Table: {table}, Column: {column}, Value: {value}')
    try:
        connection = mysql.connector.connect(user=system_info.mysql_username,
                                      password=system_info.mysql_password,
                                      host=system_info.mysql_servername,
                                      database=system_info.mysql_database)
        cursor = connection.cursor(buffered=True)
        sql_insert = "INSERT INTO " + table + " SET " + column + " = %s"
        cursor.execute(sql_insert, (value,))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as error :
        log.warning(f'Failed to insert record in database: {error}')
        exit()


def update_influx_database(measurement, value, tank_name):
    log.debug(f'update_influx_database called with (Measurement: {measurement}, Value {value}, Tank Name: {tank_name})')

    client = InfluxDBClient(system_info.influx_host, system_info.influx_port, system_info.influx_user, system_info.influx_password,
                            system_info.influx_dbname, timeout=2)
    json_body = [
        {
            "measurement": measurement,
            "tags": {
                "tank": tank_name
            },
            "fields": {
                "value": value
            }
        }
    ]
    try:
        client.write_points(json_body)
        client.close()
    except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as e:
        log.warning(f'Failed to Update record in Influx database: {e}')

    if system_info.redundant_influx:
        client2 = InfluxDBClient(system_info.influx2_host, system_info.influx2_port, system_info.influx2_user, system_info.influx2_password,
                                system_info.influx2_dbname, timeout=2)
        try:
            client2.write_points(json_body)
            client2.close()
        except (exceptions.InfluxDBClientError, exceptions.InfluxDBServerError) as e:
            log.warning(f'Failed to Update record in Influx database: {e}')


def read_influx_database(measurement, tank_name):
    log.debug(f'read_influx_database called with (Measurement: {measurement}, Tank Name: {tank_name})')
    client = InfluxDBClient(system_info.influx_host, system_info.influx_port, system_info.influx_user, system_info.influx_password, system_info.influx_dbname)
    results = client.query(("SELECT value from %s WHERE tank = %s ORDER by time DESC LIMIT 1") % (measurement, tank_name))
    points = results.get_points()
    for item in points:
        return item['value']


def main():
    print("Not intended to be run directly.")
    print("This is the system wide Influx & MySQL database module.")
    print("It is called by other modules.")
    exit()


if __name__ == '__main__':
    main()
