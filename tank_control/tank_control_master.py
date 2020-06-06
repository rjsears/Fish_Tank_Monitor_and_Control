#!/usr/bin/python3
"""
Fish Tank Control and Monitoring Program

This is the main module that runs our tank control and monitoring
program. It is intended to be called either directly as necessary
or via the crontab at whatever interval you deem necessary.
"""
__author__ = 'Richard J. Sears'
VERSION = "V1.0 (2020-06-06)"

# Handle all of our imports
import sys
sys.path.append('/var/www/fish_tank_control/tank_control/utilities')
from notifications import notify
import datetime, requests, json, system_info, http.client, power_strip, time, os, yaml
from use_database import read_mysql_database, update_mysql_database, update_influx_database, read_influx_database
from system_logging import read_logging_config
import logging.config, logging

##  Set our current timestamp & current military time
current_timestamp = int(time.time())
current_military_time = datetime.datetime.now().strftime('%A %B %d, %Y  %H:%M:%S')

## Setup all of our system logging information here:
def setup_logging(default_path='logging.yaml', default_level=logging.CRITICAL, env_key='LOG_CFG'):
    """Module to configure program-wide logging. Designed for yaml configuration files."""
    global log
    log_level = read_logging_config('logging', 'log_level')
    log = logging.getLogger(__name__)
    level = logging._checkLevel(log_level)
    log.setLevel(level)
    system_logging = read_logging_config('logging', 'system_logging')
    if system_logging:
        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                try:
                    config = yaml.safe_load(f.read())
                    logging.config.dictConfig(config)
                except Exception as e:
                    print(e)
                    print('Error in Logging Configuration. Using default configs')
                    logging.basicConfig(level=default_level)
        else:
            logging.basicConfig(level=default_level)
            print('Failed to load configuration file. Using default configs')
    else:
        log.disabled = True


# Since this system relies on external APIs (Seneye  & Thingspeak), if we do not have internet
# access there is no reason to run the script.
def check_internet():
    """Check internet access to determine if we can move forward with the rest of the script."""
    log.debug("check_internet() Started")
    check_url = system_info.check_url
    conn = http.client.HTTPConnection(check_url, timeout=3)
    try:
        conn.request("HEAD", "/")
        conn.close()
        log.debug("We have Internet Access")
        log.debug("check_internet() Completed")
        return True
    except:
        conn.close()
        log.critical("check_internet(): We 'DO NOT' have Internet Access. Exiting!")
        log.critical("check_internet() Completed with Errors. System Exit")
        exit()  # At "this" point we cannot run without internet, so just throw the error and exit.


def last_update_time(table, update_time_delta):
    """
    Calculates the time we last updated our tank reading based on calling function. Certain readings
    are only updated ever x minutes while others may be xx minutes. This function handles figuring
    out if it is time to run an update. Once calculated it will return True or False to the calling
    function. This helps with throttling requests to APIs such as Thingspeak and Seneye.
    """
    log.debug("last_update_time() Started")
    last_update_time = int(read_mysql_database(table, "last_update_time"))
    last_update_delta = (current_timestamp - int(last_update_time)) / 60
    log.debug(f"Last update was {last_update_delta:1.0f} minutes ago.")
    return last_update_delta > update_time_delta

# Module to query Seneye, download our tank data, write it to an influx database where we store our
# measurements and then update out mysql database with the last time we run an update. Since Seneye
# only updates once every 15 to 30 minutes there is no reason to continue to call their API unless
# that time has passed. The time where we update is stored in utilities/system_info.py
def get_seneye_data():
    """Queries the Seneye API for various monitored parameters and records them for use by other modules."""
    log.debug("get_seneye_data() called")
    update_time_delta = system_info.seneye_update_time
    do_seneye_update_now = last_update_time("seneye_data", update_time_delta)
    if do_seneye_update_now:
        log.debug("Time to update Seneye Readings")
        url = "https://api.seneye.com/v1/devices/76433?IncludeState=1&user={}&pwd={}".format(system_info.seneye_email, system_info.seneye_password)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        api_request = requests.get(url, headers=headers)
        response = api_request.json()
        to_json = json.dumps(response)
        dict_json = json.loads(to_json)
        keys = ['nh3', 'nh4', 'o2', 'lux', 'par', 'kelvin']
        for key in dict_json['exps']:
            if key in keys:
                value = dict_json['exps'][key]['curr']
                update_influx_database(key, float(value), system_info.tank_name)
        # Convert temperature from C to F and write both values to influx if requested
        temp_in_c = float(dict_json['exps']['temperature']['curr'])
        temp_in_f = (9.0 / 5.0 * temp_in_c) + 32
        if system_info.Temp_in_F:
            update_influx_database("temperature", temp_in_f, system_info.tank_name)
        else:
            update_influx_database("temperature", temp_in_c, system_info.tank_name)
        update_mysql_database("seneye_data", "last_update_time", current_timestamp)
    else:
        log.debug("Not time to update Seneye yet!")


def get_atlas_data():
    """
    Queries the Thingspeak API (used by the Atlas Sensors) for various monitored parameters amd records them for use by other modules.
    """
    log.debug("get_atlas_data() called")
    update_time_delta = system_info.atlas_update_time
    do_atlas_update_now = last_update_time("atlas_data", update_time_delta)
    if do_atlas_update_now:
        log.debug("Time to update Atlas Readings")
        url = "https://api.thingspeak.com/channels/{}/feed/last.json?api_key={}&results=2".format(
            system_info.thingspeak_channel, system_info.thingspeak_api_key)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        api_request = requests.get(url, headers=headers)
        response = api_request.json()
        ph = float(response['field1'])
        update_influx_database("ph", ph, system_info.tank_name)
        ec = (round(float(response['field2']),1))
        # TDS is a math function of EC, here we calculate TDS for storage or printing.
        tds = (round(float(ec * .55),1))
        update_influx_database("ec", ec, system_info.tank_name)
        update_influx_database("tds", tds, system_info.tank_name)
        temp_in_C_thingspeak = (float(response['field3']))
        update_influx_database("Temp_in_C_thingspeak", temp_in_C_thingspeak, system_info.tank_name)
        if system_info.Temp_in_F:
            temp = (round((9.0 / 5.0 * temp_in_C_thingspeak) + 32,1))
            update_influx_database("temp", temp, system_info.tank_name)
        update_mysql_database("atlas_data", "last_update_time", current_timestamp)
    else:
        log.debug("Not time to update Atlas yet!")


# When we send an alert, we don't want to keep sending it every time we run the script.
# This function checks for how often you want to send a particular alert and then sends
# it on that schedule. Timer resets when alert no longer active.
def last_alert_time(table, alert_time_delta):
    """
     Calculates the time we last sent and an alert for a particular notification.
     Prevents continuous notifications from being sent out.
     """
    last_alert_sent_time = int(read_mysql_database(table, "last_alert_sent_time"))
    last_alert_delta = (current_timestamp - int(last_alert_sent_time)) / 60
    log.debug(f"Last alert for {table} was sent {last_alert_delta:.1f} minutes ago.")
    return last_alert_delta > alert_time_delta

# Here we check tank parameters against pre-set levels in utilities/system_info.py and
# send out any necessary alerts. This particular function checks those parameters
# that have both a "low" and a "high" limit, such as PH and Temperature. Since is measures
# both a low and a high, we could use it to check other things such as water level.
def check_temp_ph_parameters(measurement, tank_name, influx_table, measurement_name):
    """Check that  pH and Temperature tank parameters are within limits. Alerts us if they are not."""
    log.debug("check_temp_ph_parameters() called")
    current_measurement = read_influx_database(influx_table, tank_name)
    log.debug(f"The current {measurement_name} of {tank_name} is {current_measurement:1.2f}")
    system_measurement_low = getattr(system_info, measurement + '_low')
    system_measurement_high = getattr(system_info, measurement + '_high')
    if current_measurement < system_measurement_low:
        measurement_alert_time = getattr(system_info, measurement + '_alert_time')
        alert_sent = read_mysql_database(measurement, "alert_sent")
        if alert_sent:
            resend_alert = last_alert_time(measurement, measurement_alert_time)
            if resend_alert:
                notify(measurement, "Fish Tank Controller", f"Your {tank_name} tank is still reporting a LOW {measurement_name} of {current_measurement}!")
                update_mysql_database(measurement, "last_alert_sent_time", current_timestamp)
                log.debug(f"{measurement_name} Alert Notification RESENT at {current_military_time}.")
            log.debug(f"Tank {measurement_name} is LOW!")
        else:
            notify(measurement, "Fish Tank Controller", f"Your {tank_name} tank has reported a LOW {measurement_name} of {current_measurement}!")
            update_mysql_database(measurement, "last_alert_sent_time", current_timestamp)
            update_mysql_database(measurement, "alert_sent", True)
            log.debug(f"{measurement_name} Alert Notification sent at {current_military_time}.")
            log.warning(f"{tank_name} has reported a LOW {measurement_name}!")
            update_mysql_database("led_status", measurement + '_low', True)
            update_mysql_database(measurement, "ok", False)
    elif current_measurement > system_measurement_high:
        measurement_alert_time = getattr(system_info, measurement + '_alert_time')
        alert_sent = read_mysql_database(measurement, "alert_sent")
        if alert_sent:
            resend_alert = last_alert_time(measurement, measurement_alert_time)
            if resend_alert:
                notify(measurement, "Fish Tank Controller",
                       f"Your {tank_name} tank is still reported a HIGH {measurement_name} of {current_measurement}!")
                update_mysql_database(measurement, "last_alert_sent_time", current_timestamp)
                log.debug(f"{measurement_name} Alert Notification RESENT at {current_military_time}.")
            log.debug(f"Tank {measurement_name} is HIGH!")
        else:
            notify(measurement, "Fish Tank Controller", f"Your {tank_name} tank has reported a HIGH {measurement_name} of {current_measurement}!")
            update_mysql_database(measurement, "last_alert_sent_time", current_timestamp)
            update_mysql_database(measurement, "alert_sent", True)
            log.debug(f"{measurement_name} Alert Notification sent at {current_military_time}.")
            log.warning(f"{tank_name} has reported a HIGH {measurement_name}!")
            update_mysql_database("led_status", measurement + '_high', True)
            update_mysql_database(measurement, "ok", False)
    else:
        ok = read_mysql_database(measurement, "ok")
        if not ok:
            update_mysql_database("led_status", measurement + '_high', False)
            update_mysql_database("led_status", measurement + '_low', False)
            update_mysql_database(measurement, "ok", True)
            update_mysql_database(measurement, "alert_sent", False)
            log.debug(f"{tank_name} has reported you are back to a NORMAL {measurement_name}!")
            notify(measurement, "Fish Tank Controller",
                   f"Your {tank_name} tank {measurement_name} is back to NORMAL, now reporting {current_measurement}!")
        log.debug(f"{tank_name} has reported a NORMAL {measurement_name}!")

# Here we check our other important parameters (nh3, nh4 & tds/ec). The parameters here only have a single
# associated value for checking, once that value is exceeded, we alert.
def check_parameters(measurement, tank_name, influx_table, measurement_name):
    """Check that  nh3, nh4 and tds/ec tank parameters are within limits. Alerts us if they are not."""
    log.debug("check_tank_parameters() called")
    current_measurement = read_influx_database(influx_table, tank_name)
    if measurement_name == 'nh3':
        log.debug(f"The current {measurement_name} of {tank_name} is {current_measurement:1.3f}")
    else:
        log.debug(f"The current {measurement_name} of {tank_name} is {current_measurement:1.0f}")
    measurement_limit = getattr(system_info, measurement)
    if current_measurement > measurement_limit:
        measurement_limit_time = getattr(system_info, measurement + '_alert_time')
        alert_sent = read_mysql_database(measurement, "alert_sent")
        if alert_sent:
            resend_alert = last_alert_time(measurement, measurement_limit_time)
            if resend_alert:
                notify(measurement, "Fish Tank Controller", f"Your {tank_name} tank is still reported a HIGH {measurement_name} of {current_measurement}!")
                update_mysql_database(measurement, "last_alert_sent_time", current_timestamp)
                log.debug(f"{measurement_name} Alert Notification RESENT at {current_military_time}.")
            log.warning(f"Tank {measurement_name} is LOW!")
        else:
            notify(measurement, "Fish Tank Controller", f"Your {tank_name} tank has reported a HIGH {measurement_name} of {current_measurement}!")
            update_mysql_database(measurement, "last_alert_sent_time", current_timestamp)
            update_mysql_database(measurement, "alert_sent", True)
            log.debug(f"{measurement_name} Alert Notification sent at {current_military_time}.")
            log.warning(f"{tank_name} has reported a HIGH {measurement_name}!")
            update_mysql_database("led_status", measurement, True)
            update_mysql_database(measurement, "ok", False)
    else:
        ok = read_mysql_database(measurement, "ok")
        if not ok:
            update_mysql_database("led_status", measurement, False)
            update_mysql_database(measurement, "ok", True)
            update_mysql_database(measurement, "alert_sent", False)
            log.debug(f"{tank_name} has reported you are back to a NORMAL {measurement_name}!")
            notify(measurement, "Fish Tank Controller", f"Your {tank_name} tank {measurement_name} is back to NORMAL, now reporting {current_measurement}!")
        log.debug(f"{tank_name} has reported a NORMAL {measurement_name}!")

# The following functions utilize realtime power readings to verify that
# the equipment is actually running and not just "turned on". Right now,
# we utilize this information to toggle our "led" indicators on our web
# control panel. Eventually will be expanded to more intelligently determine
# if we need to power cycle equipment.

def check_airpump_status():
    """Check if our air pump is physically running."""
    log.debug("check_airpump_status() called")
    airpump_current_watts = power_strip.get_current_power("Air Pump")
    if airpump_current_watts > system_info.air_pump_watts:
        update_mysql_database("led_status", "airpump_status", True)
    else:
        update_mysql_database("led_status", "airpump_status", False)

def check_uv_pump_status():
    """Check if our UV light and pump is physically running."""
    log.debug("check_uv_pump_status() called")
    uv_pump_current_watts = power_strip.get_current_power("UV Light")
    if uv_pump_current_watts > system_info.uv_pump_watts:
        update_mysql_database("led_status", "uv_pump_status", True)
    else:
        update_mysql_database("led_status", "uv_pump_status", False)

def check_fx6_filter_status():
    """Check if our FX6 filter is physically running."""
    log.debug("check_fx6_filter_status() called")
    fx6_filter_current_watts = power_strip.get_current_power("FX6 Filter")
    if fx6_filter_current_watts > system_info.fx6_filter_watts:
        update_mysql_database("led_status", "fx6_status", True)
    else:
        update_mysql_database("led_status", "fx6_status", False)

def check_406_filter_status():
    """Check if our 406 filter is physically running."""
    log.debug("check_406_filter_status() called")
    f406_filter_current_watts = power_strip.get_current_power("406 Filter")
    if f406_filter_current_watts > system_info.f406_filter_watts:
        update_mysql_database("led_status", "f406_status", True)
    else:
        update_mysql_database("led_status", "f406_status", False)

def check_ph_controller_status():
    """Check if our pH Controller is physically running."""
    log.debug("check_ph_controller_status() called")
    ph_controller_current_watts = power_strip.get_current_power("PH Controller")
    if ph_controller_current_watts > system_info.ph_controller_watts:
        update_mysql_database("led_status", "injecting_co2_led", True)
    else:
        update_mysql_database("led_status", "injecting_co2_led", False)

def get_sensor_data():
    """Collect sensor data."""
    log.debug("get_sensor_data() called")
    get_seneye_data()
    get_atlas_data()

def check_readings():
    """Check readings to make sure all parameters are within limits."""
    log.debug("check_readings() called")
    for parameter in ["ph", "temp"]:
        check_temp_ph_parameters(parameter + "_status", "'75planted'", parameter, parameter)
    for parameter in ["nh3", "nh4", "tds"]:
        check_parameters(parameter + "_status", "'75planted'", parameter, parameter)

def check_equipment_status():
    """Verify that our equipment is running as required."""
    log.debug("check_equipment_status() called")
    check_airpump_status()
    check_uv_pump_status()
    check_fx6_filter_status()
    check_406_filter_status()
    check_ph_controller_status()

def main():
    setup_logging()
    log.info("tank_control_master() Starting.")
    check_internet()
    get_sensor_data()
    check_readings()
    check_equipment_status()
    log.info("tank_control_master() Completed.")


if __name__ == '__main__':
    main()