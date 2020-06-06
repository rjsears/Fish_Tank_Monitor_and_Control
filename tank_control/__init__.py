#!/usr/bin/python3

__author__ = 'Richard J. Sears'
VERSION = "V1.0 (2020-06-06)"

## Utilizes sentry.io, remove if not needed or update creds
## if you use it.

import sys
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
sys.path.append('/var/www/fish_tank_control/tank_control/utilities')
from flask import Flask

sentry_sdk.init(
    dsn="https://xxxxxxxxxxxxxxxxxxxxxxxx@sentry.io/xxxxxxxxx",
    integrations=[FlaskIntegration()])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sjdfgisfijsijhfidshifs8sd8f8sdf'

# Must import AFTER the above otherwise you will get a circular reference
# due to the fact that routes.py imports the app stuff.

from tank_control import routes
