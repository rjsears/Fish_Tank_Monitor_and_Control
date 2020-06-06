#!/usr/bin/python3

__author__ = 'Richard J. Sears'
VERSION = "V1.0.0 (2020-06-06)"
# richardjsears@gmail.com

## Functions that allow interaction with my Kasa Smart PowerStrip.
## This uses a Class forked from https://github.com/p-doyle/Python-KasaSmartPowerStrip

# See here for available commands
#https://github.com/rjsears/Python-KasaSmartPowerStrip/blob/master/KasaSmartPowerStrip.py

from KasaSmartPowerStrip import SmartPowerStrip
import system_info
import logging
from system_logging import read_logging_config

# Setup module Logging. Main setup is done in tank_control_master.py
level = read_logging_config('logging', 'log_level')
level = logging._checkLevel(level)
log = logging.getLogger(__name__)
log.setLevel(level)

power_strip = SmartPowerStrip(system_info.tank_name)

def get_current_power(plug_name):
    log.debug(f'get_current_power() called with ({plug_name})')
    current_power_readings = power_strip.get_realtime_energy_info(plug_name = plug_name)
    current_power_watts = round((current_power_readings['power_mw'] / 1000), 1)
    log.debug(f'get_current_power({plug_name}) returned: {current_power_watts}')
    return current_power_watts


def toggle_plug_power(plug_name, state):
    log.debug(f'toggle_power_plug() called with ({plug_name}, {state})')
    power_strip.toggle_plug(state, plug_name = plug_name)

def get_plug_info(plug_number):
    log.debug(f'get_plug_info() called with ({plug_number})')
    p_info = power_strip.get_plug_info(plug_number)
    plug_info = p_info[0]
    log.debug(f'get_plug_info({plug_number}) returned: {plug_info}')
    return (plug_info)

