# -*- coding: utf-8 -*-

from time_switch.model import SwitchModel
from time_switch.manager import SwitchManager

import argparse
import logging
import atexit


parser = argparse.ArgumentParser(description='Timeswitch for the\
 GPIOs of an Raspberry Pi.')
parser.add_argument('--file', dest='schedule_file', metavar='file',
					type=str, default='gpio_time.db',
					help='A JSON-file containing the schedule.')

args = parser.parse_args()

switch_model = SwitchModel(args.schedule_file)
switch_manager = SwitchManager(switch_model)

switch_manager.start()

def exit_handler():
    switch_manager.stop()

atexit.register(exit_handler)
