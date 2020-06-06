#!/usr/bin/python3

import sys
sys.path.append('/var/www/fish_tank_control/tank_control/utilities')
from flask import render_template, redirect, url_for, request
from use_database import update_mysql_database, read_mysql_database, read_influx_database, update_influx_database
from tank_control.forms import ParameterForm
import system_info
from power_strip import toggle_plug_power
from tank_control import app


@app.route('/')
def tank_control():
    # Get current tank Parameters
    current_parameters_keys = ['temp', 'ph', 'nh3', 'nh4', 'ec',
                               'tds', 'o2', 'par', 'lux', 'kelvin']
    parameter_data = {}
    for key in current_parameters_keys:
        parameter_data[key] = read_influx_database(key, "'75planted'")

    # Check Status
    led_status = ['tank_overall_status_led', 'temp_status_high',
                                  'temp_status_low', 'ph_status_low', 'ph_status_high',
                                  'nh3_status', 'tds_status', 'injecting_co2_led',
                                  'fx6_status','f406_status', 'airpump_status', 'uv_pump_status']
    led_data = {}
    for key in led_status:
        led_data[key] = read_mysql_database("led_status", key)

    # Get Power Readings
    current_power_keys = ['total_current_power_utilization', 'total_current_power_import',
                          'total_current_solar_production']
    power_data = {}
    for key in current_power_keys:
        power_data[key] = read_mysql_database("power_solar", key)


    current_military_time = read_mysql_database("system_status", "current_military_time")

    return render_template('index.html',
            **parameter_data, **led_data, **power_data,
            current_military_time = current_military_time)


@app.route('/notifications')
def notifications():
    # Grab Notification Settings
    notification_keys = ['ph_status_sms', 'ph_status_pb', 'ph_status_email',
            'fx6filter_status_sms', 'fx6filter_status_pb', 'fx6filter_status_email',
            'f406filter_status_sms', 'f406filter_status_pb', 'f406filter_status_email',
            'uv_status_sms', 'uv_status_pb', 'uv_status_email',
            'phcontroller_status_sms', 'phcontroller_status_pb', 'phcontroller_status_email',
            'airpump_status_sms', 'airpump_status_pb', 'airpump_status_email',
            'temp_status_sms', 'temp_status_pb', 'temp_status_email',
            'waterlevel_status_sms', 'waterlevel_status_pb', 'waterlevel_status_email',
            'nh3_status_sms', 'nh3_status_pb', 'nh3_status_email',
            'tds_status_sms', 'tds_status_pb', 'tds_status_email',
            'system_wide', 'edit_notifications']
    notification_data = {}
    for key in notification_keys:
        notification_data[key] = read_mysql_database("notifications", key)
    system_logging = read_mysql_database("logging", "system_logging" )
    log_level = read_mysql_database("logging", "log_level")

    return render_template('notifications.html', **notification_data,
                           system_logging = system_logging,
                           log_level = log_level)



@app.route('/parameters', methods=['GET', 'POST'])
def parameters():
    form = ParameterForm()
    if form.validate_on_submit():
        results = request.form
        keys = ['gh', 'kh', 'po4']
        for key,value in results.items():
            if key in keys:
                update_influx_database(key, float(value), system_info.tank_name)
        return redirect(url_for('success'))
    return render_template('parameters.html', form = form)

@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('success.html',
                           template='success-template')


@app.route('/notifications_systemwide')
def toggle_notifications_systemwide():
    notifications_systemwide = read_mysql_database("notifications", "system_wide")
    if notifications_systemwide:
        update_mysql_database("notifications", "system_wide", False)
        update_mysql_database("notifications", "edit_notifications", False)
    else:
        update_mysql_database("notifications", "system_wide", True)
    return redirect(url_for('notifications'))

@app.route('/edit_notifications_menu')
def toggle_edit_notifications_menu():
    edit_notifications_menu = read_mysql_database("notifications", "edit_notifications")
    if edit_notifications_menu:
        update_mysql_database("notifications", "edit_notifications", False)
    else:
        update_mysql_database("notifications", "edit_notifications", True)
    return redirect(url_for('notifications'))

@app.route('/modify_notifications/<notifications>', methods=['GET'])
def modify_notifications(notifications):
    current_notification_setting = read_mysql_database("notifications", notifications)
    if current_notification_setting:
        update_mysql_database("notifications", notifications, False)
    else:
        update_mysql_database("notifications", notifications, True)
    return redirect(url_for('notifications'))

@app.route('/airpump_power')
def toggle_airpump_power():
    airpump_status = read_mysql_database("led_status", "airpump_status")
    if airpump_status:
        toggle_plug_power('Air Pump', 'off')
        update_mysql_database("led_status", "airpump_status", False)
        return redirect(url_for('tank_control'))
    else:
        toggle_plug_power('Air Pump', 'on')
        update_mysql_database("led_status", "airpump_status", True)
        return redirect(url_for('tank_control'))

@app.route('/fx6_power')
def toggle_fx6_power():
    fx6_status = read_mysql_database("led_status", "fx6_status")
    if fx6_status:
        toggle_plug_power('FX6 Filter', 'off')
        update_mysql_database("led_status", "fx6_status", False)
        return redirect(url_for('tank_control'))
    else:
        toggle_plug_power('FX6 Filter', 'on')
        update_mysql_database("led_status", "fx6_status", True)
        return redirect(url_for('tank_control'))

@app.route('/406_power')
def toggle_406_power():
    f406_status = read_mysql_database("led_status", "406_status")
    if f406_status:
        toggle_plug_power('406 Filter', 'off')
        update_mysql_database("led_status", "406_status", False)
        return redirect(url_for('tank_control'))
    else:
        toggle_plug_power('406 Filter', 'on')
        update_mysql_database("led_status", "406_status", True)
        return redirect(url_for('tank_control'))

@app.route('/uv_pump_power')
def toggle_uv_pump_power():
    uv_pump_status = read_mysql_database("led_status", "uv_pump_status")
    if uv_pump_status:
        toggle_plug_power('UV Light', 'off')
        update_mysql_database("led_status", "uv_pump_status", False)
        return redirect(url_for('tank_control'))
    else:
        toggle_plug_power('UV Light', 'on')
        update_mysql_database("led_status", "uv_pump_status", True)
        return redirect(url_for('tank_control'))

@app.route('/ph_controller_power')
def toggle_ph_controller_power():
    ph_controller_status = read_mysql_database("led_status", "injecting_co2_led")
    if ph_controller_status:
        toggle_plug_power('PH Controller', 'off')
        update_mysql_database("led_status", "injecting_co2_led", False)
        return redirect(url_for('tank_control'))
    else:
        toggle_plug_power('PH Controller', 'on')
        update_mysql_database("led_status", "injecting_co2_led", True)
        return redirect(url_for('tank_control'))

@app.route('/toggle_logging')
def toggle_logging():
    system_logging = read_mysql_database("logging", "system_logging" )
    if system_logging:
        update_mysql_database("logging", "system_logging", False)
    else:
        update_mysql_database("logging", "system_logging", True)
    return redirect(url_for('notifications'))

@app.route('/debug')
def toggle_debug():
    log_level = read_mysql_database("logging", "log_level" )
    if log_level == 'DEBUG':
        update_mysql_database("logging", "log_level", 'INFO')
    else:
        update_mysql_database("logging", "log_level", 'DEBUG')
    return redirect(url_for('notifications'))


# This allows us to call static pages utilizing Flask as opposed to Apache.
@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)
