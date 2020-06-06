#!/usr/bin/python3

__author__ = 'Richard J. Sears'
VERSION = "V1.0 (2020-06-06)"

from tank_control import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)