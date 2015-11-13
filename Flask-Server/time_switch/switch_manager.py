#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time_switch.model import is_relative_time, is_absolute_time
import logging
import threading
import time
import random

class NullHandler(logging.Handler):
    '''Logging Handler which makes all logging
        calls silent, if the user of the module did
        not specifies an other handler.'''

    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
except ImportError:
    LOGGER.warning('Running with gpio mockup! RPi.GPIO not installed?')
    import time_switch.no_gpio as GPIO

SWITCH_ON = GPIO.HIGH
SWITCH_OFF = GPIO.LOW

UNIT_PER_MINUTE = 1
UNIT_PER_HOUR = 60
UNIT_PER_DAY = 24 * 60

def time_in_sequence(start_tm, end_tm, cur_tm):
    """Returns true if cur_time is in the range [start, end]."""
    if end_tm == start_tm:
        return False
    elif cur_tm < end_tm and end_tm < start_tm:
        return True # Morning.[cur].[end] [start].evening
    elif end_tm < start_tm and start_tm <= cur_tm:
        return True # Morning.[end] [start].[cur].evening
    elif start_tm <= cur_tm and cur_tm < end_tm:
        return True # Morning [start]..[cur].[end] evening

    return False

def is_sequence_active(start_tm, end_tm):
    '''Checks if the current time lays in this sequence.'''
    time_struct = time.localtime()
    cur_time = time_struct.tm_hour * UNIT_PER_HOUR + time_struct.tm_min * UNIT_PER_MINUTE
    return time_in_sequence(start_tm, end_tm, cur_time)

def pars_rel_time(time_str):
    '''Takes a time string and converts it to an integer.

        The string should have the format HH:MM. The returned
        integer represents the passed minutes.'''

    if not is_relative_time(time_str):
        raise TypeError("Expected a relativ time. A string\
 representing an integer between 0 and 1440. Got: " + time_str)
    return int(time_str)

def pars_abs_time(time_str):
    '''Takes a string and converts it to an integer.'''
    if not is_absolute_time(time_str):
        raise TypeError("Expected an absulute time (HH:MM). Got: " + time_str)
    time_struct = time.strptime(time_str, "%H:%M")
    return time_struct.tm_hour * UNIT_PER_HOUR + time_struct.tm_min * UNIT_PER_MINUTE

class SwitchManager(object):
    '''This class manages the GPIO pins.'''
    def __init__(self, switch_model):
        self.switch_model = switch_model
        self.pins = self.switch_model.get_pins()
        self.gpios = {}
        self.diffusions = {}
        self.event = threading.Event()
        self.thread = threading.Thread(target=self._loop, args=())

    def get_model(self):
        '''Returns the current used model.'''
        return self.switch_model

    def _get_diffusioned_intervall(self, sequence):
        '''Returns a tuple of start and end time.'''
        sequence_id = sequence.get_id()
        end_tm_str = sequence.get_end()
        start_tm_str = sequence.get_start()

        if sequence_id not in self.diffusions:
            if is_relative_time(start_tm_str[0]):
                print str(start_tm_str)
                start_tm = (pars_rel_time(start_tm_str[0]), pars_rel_time(start_tm_str[1]))
                end_tm = (pars_abs_time(end_tm_str[0]), pars_rel_time(end_tm_str[1]))

                rand_end = end_tm[0]
                if end_tm[1] != 0:
                    rand_end += random.randint(-end_tm[1], end_tm[1])

                duration = start_tm[0]
                if start_tm[1] != 0:
                    duration += random.randint(-start_tm[1], start_tm[1])
                rand_start = (rand_end - duration) % UNIT_PER_DAY

                if duration <= 0:
                    rand_start = rand_end

                self.diffusions[sequence_id] = (rand_start, rand_end)

            elif is_relative_time(end_tm_str[0]):
                start_tm = (pars_abs_time(start_tm_str[0]), pars_rel_time(start_tm_str[1]))
                end_tm = (pars_rel_time(end_tm_str[0]), pars_rel_time(end_tm_str[1]))

                rand_start = start_tm[0] + random.randint(-start_tm[1], start_tm[1])
                duration = end_tm[0] + random.randint(-end_tm[1], end_tm[1])
                rand_end = (rand_start + duration) % UNIT_PER_DAY

                if duration <= 0:
                    rand_end = rand_start

                self.diffusions[sequence_id] = (rand_start, rand_end)
            else:
                start_tm = (pars_abs_time(start_tm_str[0]), pars_rel_time(start_tm_str[1]))
                end_tm = (pars_abs_time(end_tm_str[0]), pars_rel_time(end_tm_str[1]))

                rand_start = start_tm[0] + random.randint(-start_tm[1], start_tm[1])

                rand_end = end_tm[0] + random.randint(-end_tm[1], end_tm[1])

                tm_diff = end_tm[0] - start_tm[0]
                rand_tm_diff = rand_end - rand_start

                if tm_diff * rand_tm_diff <= 0:
                    rand_start = rand_end

                self.diffusions[sequence_id] = (rand_start, rand_end)

        return self.diffusions[sequence_id]

    def update_all_gpios(self):
        """Updates all GPIOs according to the schedule."""
        for pin in self.pins: # iterate through all pins and update them
            self.update_gpio_state(pin) # update GPIO state

    def update_gpio_state(self, pin):
        """Changes the state of the GPIO to high or low according to the schedule."""
        active_sequence_found = False

        for sequence in pin.get_sequences(): # iterate through all squences.
            intervall = self._get_diffusioned_intervall(sequence)
            if is_sequence_active(*intervall): # if in sequence
                active_sequence_found = True # set found true
                break # and leave the loop

        pin_id = pin.get_id()
        if active_sequence_found:
            self.switch_pin_on(pin_id)
        elif not active_sequence_found:
            self.switch_pin_off(pin_id)

    def switch_pin_on(self, pin_id):
        if pin_id not in self.gpios:
            GPIO.setup(pin_id, GPIO.OUT) # setup GPIO
        self.gpios[pin_id] = True
        GPIO.output(pin_id, SWITCH_ON)

    def switch_pin_off(self, pin_id):
        if pin_id not in self.gpios:
            GPIO.setup(pin_id, GPIO.OUT) # setup GPIO
        self.gpios[pin_id] = False
        GPIO.output(pin_id, SWITCH_OFF)

    def state_for_gpio(self, pin_id):
        if pin_id not in self.gpios:
            return False
        else:
            return self.gpios[pin_id]

    def start(self):
        '''Starts the timeswitch and sets the GPIOs up.'''
        GPIO.setmode(GPIO.BOARD)
        self.thread.start()

    def stop(self):
        '''Stops the timeswitch and cleansup the GPIOs.'''
        self.event.set()
        GPIO.cleanup()
        self.gpios.clear()

    def _loop(self):
        '''Tests every minute if a GPIO should be switcht on or off.'''
        cur_day = time.gmtime().tm_yday
        while not self.event.is_set(): # loop until (event is set -> thread should stop)
            self.pins = self.switch_model.get_pins() # update model

            if cur_day != time.gmtime().tm_yday: # if new day started
                cur_day = time.gmtime().tm_yday # update current day
                self.diffusions.clear() # delete all times -> Calculate new random times.

            self.update_all_gpios() # update GPIOs
            self.event.wait(61 - time.localtime().tm_sec) # wait a minute

        self.event.clear()
