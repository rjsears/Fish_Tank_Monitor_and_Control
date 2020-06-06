#!/usr/bin/python3


__author__ = 'Richard J. Sears'
VERSION = "V1.0.0 (2020-06-06)"
# richardjsears@gmail.com

# Part of my Fish Tank Control suite of scripts and hardware to
# monitor and manage my fish tank.

# notifications.py
# Main Notifications module that handles all logging and notifications system
# wide. This resides in the Utilities directory.

# Notify
# This function reads notification configurations and provides notification for the following:
# E-Mail (alert email set in system_info.py)
# Pushbullet
# Twilio (SMS)

# This script is not intended to be run manually, rather it is called by other modules.


import time
import logging
import subprocess
from pushbullet import Pushbullet
from twilio.rest import Client
import system_info
import mysql.connector
from mysql.connector import Error
from system_logging import read_logging_config

# Setup module Logging. Main setup is done in tank_control_master.py
level = read_logging_config('logging', 'log_level')
level = logging._checkLevel(level)
log = logging.getLogger(__name__)
log.setLevel(level)


## We need to have our database functions here instead of calling use_database.py
## This resolves an circular import issue.


def read_mysql_database(table, column):
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
        log.warning(f'Failed to read record from database: {error}')
        exit()
    finally:
        if(connection.is_connected()):
            connection.close
            #log("INFO", "use_database.py:read_mysql_database() Database connection closed.")

def update_mysql_database(table,column,value):
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

        log.warning(f"Failed to UPDATE database: {error}")
        exit()
    finally:
        if(connection.is_connected()):
            connection.close


current_timestamp = int(time.time())


# Setup to send email via the builtin linux mail command.
# Your local system must be configured already to send mail or this will fail.
def send_email(recipient, subject, body):
    process = subprocess.Popen(['mail', '-s', subject, recipient],stdin=subprocess.PIPE)
    process.communicate(body)

# Setup to send out Pushbillet alerts. Pushbullet config is in pooldb.py
def send_push_notification(title, message):
    pb = Pushbullet(system_info.pushbilletAPI)
    push = pb.push_note(title, message)

# Setup to send SMS Text messages via Twilio. Configured in pooldb.py
def send_sms_notification(body):
    client = Client(system_info.twilio_account, system_info.twilio_token)
    message = client.messages.create(to=system_info.twilio_to, from_=system_info.twilio_from,
                                         body=body)


# Notify system for email, pushbullet and sms (via Twilio)
def notify(sub_system_notifications, title, message):
    system_wide_notifications = read_mysql_database("notifications", "system_wide")
    if system_wide_notifications:
        email = read_mysql_database("notifications", sub_system_notifications + '_email')
        pushbullet = read_mysql_database("notifications", sub_system_notifications + '_pb')
        sms = read_mysql_database("notifications", sub_system_notifications + '_sms')

        if pushbullet:
            send_push_notification(title,message)
            log.debug(f"Pushbullet Notification Sent: {title} - {message}")
        else:
            pass

        if email:
            send_email(system_info.alert_email, title, message)
            log.debug(f"Email Notification Sent: {title} - {message}")
        else:
            pass

        if sms:
            send_sms_notification(message)
            log.debug(f"SMS Notification Sent: {message}.")
        else:
            pass
    else:
        pass

def main():
    print("Not intended to be run directly.")
    print("This is the systemwide Notification module.")
    print("It is called by other modules.")
    exit()


if __name__ == '__main__':
    main()
