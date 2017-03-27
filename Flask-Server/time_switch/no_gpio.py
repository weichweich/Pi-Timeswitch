#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)

LOW = 0
HIGH = 1
IN = 'in'
OUT = 'out'
BOARD = 'board'

pins = {}

def input(pinNum):
    if pinNum in pins:
        return pins[pinNum]
    return LOW

def output(pinNum, voltage):
    pins[pinNum] = voltage
    LOGGER.debug('Swtich pin {0:d} -> {1} '.format(pinNum, voltage))

def setmode(mode):
    LOGGER.debug('GPIO mode: {0:s}'.format(mode))

def setup(pin, pinType, initial=HIGH):
    output(pin, HIGH)
    LOGGER.debug('Pin {0:d} is set to {1:s}'.format(pin, pinType))

def cleanup(*args, **kwargs):
    LOGGER.debug('cleanup args: ' + str(args) + ' |kwargs: ' + str(kwargs))
