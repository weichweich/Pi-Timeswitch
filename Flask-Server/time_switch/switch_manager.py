#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time_switch.model import is_relative_time, is_absolute_time, SWITCH_OFF, SWITCH_ON, SWITCH_UNDEF
import logging
import threading
import time
import random

time.strptime('2012-01-01', '%Y-%m-%d') # dummy call to prevent error...

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
    LOGGER.warning('Error importing RPi.GPIO! Running with gpio mockup! RPi.GPIO not installed?')
    import time_switch.no_gpio as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


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

def parse_rel_time(time_str):
    '''Takes a string representing an integer in range 0, 1440.'''
    if not is_relative_time(time_str):
        raise TypeError("Expected a relativ time. A string\
 representing an integer between 0 and 1440. Got: " + time_str)
    return int(time_str)

def parse_abs_time(time_str):
    '''Takes a time string and converts it to an integer.

        The string should have the format HH:MM. The returned
        integer represents the passed minutes.'''
    if not is_absolute_time(time_str):
        raise TypeError(u"Expected an absulute time (HH:MM). Got: " + time_str)
    time_struct = time.strptime(time_str, "%H:%M")
    return time_struct.tm_hour * UNIT_PER_HOUR + time_struct.tm_min * UNIT_PER_MINUTE

class SwitchManager(object):
    '''This class manages the GPIO pins.'''
    def __init__(self, switch_model):
        self.switch_model = switch_model
        self.used_gpios = []
        self.manual_switched = {}
        self.diffusions = {}
        self.event = threading.Event()
        self.thread = threading.Thread(target=self.__loop, args=())
        self.thread_running=False

    def get_model(self):
        '''Returns the current used model.'''
        return self.switch_model

    def update(self):
        pins = self.switch_model.get_pins()
        
        # find deleted pins
        deleted_pins = self.used_gpios[:]
        for pin in pins:
            if pin.get_id() in deleted_pins:
                deleted_pins.remove(pin.get_id())

        # update the other pins
        self.update_all_gpios()

    def _get_diffusioned_intervall(self, sequence):
        '''Returns a tuple of start and end time.'''
        sequence_id = sequence.get_id()
        end_tm_str = sequence.get_end()
        start_tm_str = sequence.get_start()

        if sequence_id not in self.diffusions:
            # if deffusion is not calculated:

            if is_relative_time(start_tm_str[0]):
                # if start is relativ to the end time

                # parse start and end time
                start_tm = (parse_rel_time(start_tm_str[0]), parse_rel_time(start_tm_str[1]))
                end_tm = (parse_abs_time(end_tm_str[0]), parse_rel_time(end_tm_str[1]))

                # calculate randomized end time
                rand_end = end_tm[0]
                if end_tm[1] != 0:
                    rand_end += random.randint(-end_tm[1], end_tm[1])
                    rand_end %= UNIT_PER_DAY

                # calculate start time depending on end.
                duration = start_tm[0]
                if start_tm[1] != 0: # randomize start time if nessesary
                    duration += random.randint(-start_tm[1], start_tm[1])
                rand_start = (rand_end - duration) % UNIT_PER_DAY

                if duration <= 0:
                    rand_start = rand_end

                self.diffusions[sequence_id] = (rand_start, rand_end)

            elif is_relative_time(end_tm_str[0]):
                # if end is relativ to start time

                # parse start and end time
                start_tm = (parse_abs_time(start_tm_str[0]), parse_rel_time(start_tm_str[1]))
                end_tm = (parse_rel_time(end_tm_str[0]), parse_rel_time(end_tm_str[1]))

                # calculate
                rand_start = start_tm[0]
                if start_tm[1] != 0:
                    rand_start += random.randint(-start_tm[1], start_tm[1])
                    rand_start %= UNIT_PER_DAY

                # calculate end time depending on start.
                duration = end_tm[0]
                if end_tm[1] != 0: # randomize end time if nessesary
                    duration += random.randint(-end_tm[1], end_tm[1])
                rand_end = (rand_start + duration) % UNIT_PER_DAY

                if duration <= 0:
                    rand_end = rand_start

                self.diffusions[sequence_id] = (rand_start, rand_end)
            else:
                # if both are absolute times.
                start_tm = (parse_abs_time(start_tm_str[0]), parse_rel_time(start_tm_str[1]))
                end_tm = (parse_abs_time(end_tm_str[0]), parse_rel_time(end_tm_str[1]))

                # calculate start
                rand_start = start_tm[0] + random.randint(-start_tm[1], start_tm[1])

                # calculate end
                rand_end = end_tm[0] + random.randint(-end_tm[1], end_tm[1])

                # calculate duration of on time befor and after randomization
                tm_diff = end_tm[0] - start_tm[0]
                rand_tm_diff = rand_end - rand_start

                # if order of start and end time switched, make the sequence disapear.
                # [morning]--[start]+++[end]---[evening] => [morning]++[end]--[start]++[evening]
                if tm_diff * rand_tm_diff <= 0:
                    rand_start = rand_end

                self.diffusions[sequence_id] = (rand_start, rand_end)

        return self.diffusions[sequence_id]

    def update_all_gpios(self):
        """Updates all GPIOs according to the schedule."""
        pins = self.switch_model.get_pins()
        for pin in pins: # iterate through all pins and update them
            self.update_gpio_state(pin) # update GPIO state

    def update_gpio_state(self, pin):
        """Changes the state of the GPIO to high or low according to the schedule."""
        active_sequence_found = False

        for sequence in pin.sequences: # iterate through all squences.
            intervall = self._get_diffusioned_intervall(sequence)
            if is_sequence_active(*intervall): # if in sequence
                active_sequence_found = True # set found true
                break # and leave the loop

        if active_sequence_found:
            self.__switch_pin_on(pin)
        elif not active_sequence_found:
            self.__switch_pin_off(pin)

    def __switch_pin_on(self, pin):
        self.switch_model.switch_pin_on(pin)

    def __switch_pin_off(self, pin):
        self.switch_model.switch_pin_off(pin)


    def start(self):
        '''Starts the timeswitch and sets the GPIOs up.'''
        LOGGER.info("Start gpio manager")
        if not self.thread_running:
            self.thread.start()
            self.thread_running = True

    def stop(self):
        '''Stops the timeswitch and cleansup the GPIOs.'''
        LOGGER.info("stop gpio manager")
        self.event.set()
        self.thread_running = False

    def __loop(self):
        '''Tests every minute if a GPIO should be switcht on or off.'''
        cur_day = time.gmtime().tm_yday
        while not self.event.is_set(): # loop until (event is set -> thread should stop)
            if cur_day != time.gmtime().tm_yday: # if new day started
                cur_day = time.gmtime().tm_yday # update current day
                self.diffusions.clear() # delete all times -> Calculate new random times.

            self.update_all_gpios() # update GPIOs
            self.event.wait(60) # wait a minute

        self.event.clear()
