#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)

LOW = 'low'
HIGH = 'high'
IN = 'in'
OUT = 'out'
BOARD = 'board'

def output(pinNum, voltage):
    LOGGER.debug('Swtich pin {0:d} -> {1:s} '.format(pinNum, voltage))

def setmode(mode):
    LOGGER.debug('GPIO mode: {0:s}'.format(mode))

def setup(pin, pinType):
	LOGGER.debug('Pin {0:d} is set to {1:s}'.format(pin, pinType))

def cleanup():
	LOGGER.debug('cleanup')
