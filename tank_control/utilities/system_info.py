#!/usr/bin/python3

# System wide information file that holds credentials for database and other connections.

__author__ = 'Richard J. Sears'
VERSION = "V1.0.0 (2020-06-06)"
# richard@sears.net


    
# URL that we use to check and see if we have internet connectivity.
check_url = 'www.google.com'

# This is useful if you have multiple tanks you want to keep track of...
tank_name = '75planted'

# Do we want to store our temperatures in F or C?
# If you are like me and want to see your tank water temperature in Fahrenheit, set to True
Temp_in_F = True

# Here is all of our MySQL Connection information
mysql_servername = "localhost"
mysql_username = "fishtank"  # Your main MySQL admin username or username that is the exact same for both databases
mysql_password = "password_here"  # Your main MySQL admin password or password that is exact same for both databases
mysql_database = "fishtanks_75planted"  # The name of your fish tank  (or other) database.

# Do we operate redundant InfluxDB Servers:
redundant_influx = True

## Information for our Influx Databases:
influx_host = 'influx01'
influx_port = 8086
influx_user = 'fish_tank'
influx_password = 'password'
influx_dbname = 'fish_tank'

# Second InfluxDB connections settings (only used if 'redundant_influx = True' is set above.
influx2_host = 'influx02.domain.com'
influx2_port = 8086
influx2_user = 'fish_tank'
influx2_password = 'password'
influx2_dbname = 'fish_tank'



## Info for our notifications.py
## Set Notification Accounts#
alert_email = 'your_email@gmail.com'
twilio_from = '+18585551212'
twilio_account = 'your_account_number_here'
twilio_token = 'your_tken_here'
twilio_to = '+18585551212'
pushbilletAPI = "your.api.token.here"  # pushbullet API token (http://www.pushbullet.com)

#Seneye Settings
seneye_email = "your_email@gmail.com"
seneye_password = "password"
seneye_update_time = 10

# ThingSpeak API Settings for Atlas probes
thingspeak_api_key = "your_api_key_here"
thingspeak_channel = "000000"
atlas_update_time = 1

# Tank Alert Levels - set your alert levels here
nh3_status = 0.05
nh3_status_alert_time = 60

nh4_status = 1500
nh4_status_alert_time = 60

tds_status = 500
tds_status_alert_time = 60

ph_status_low = 5.5
ph_status_high = 7.4
ph_status_alert_time = 60

# TODO Deal with hysteresis
temp_status_low = 77
temp_status_high = 85
temp_status_alert_time = 60


#Power Utilization Settings (in watts)
air_pump_watts = .3
uv_pump_watts = 25
fx6_filter_watts = 40
f406_filter_watts = 18
ph_controller_watts = .3


# Power Strip Mapping name to outlet number for power readings
ph_controller = 1
fx6_filter = 2
f406_filter = 3
uv_light = 4
air_pump = 5
temp_controller = 6


def main():
    print("This script is not intended to be run directly.")
    print("This is the systemwide Credentials & Settings module.")
    print("It is called by other modules.")
    exit()


if __name__ == '__main__':
    main()
