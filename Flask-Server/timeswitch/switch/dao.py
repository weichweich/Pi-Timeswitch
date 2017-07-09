# -*- coding: utf-8 -*-

SWITCH_ON = 1
SWITCH_OFF = 0
SWITCH_UNDEF = -1

class Sequence(object):
    def __init__(self, start_time, start_range, end_time,
                 end_range, pin=None, sequence_id=-1):
        self.pin = pin
        self.id = sequence_id

        if (type(start_range) is int):
            start_range = str(start_range)
        if (type(end_range) is int):
            end_range = str(end_range)

        if (type(start_time) is int):
            start_time = str(start_time)
        if (type(end_time) is int):
            end_time = str(end_time)

        self.start_time = start_time
        self.start_range = start_range
        self.end_time = end_time
        self.end_range = end_range

    def get_pin(self):
        return self.pin

    def set_pin(self, pin):
        self.pin = pin
        if (self.pin):
            self.pin_id = pin.get_id()

    def get_id(self):
        return self.id

    def set_id(self, sequence_id):
        self.id = sequence_id

    def get_start(self):
        return (self.start_time, self.start_range)

    def set_start(self, start_time, start_range):
        self.start_time, self.start_range = start_time, start_range

    def get_end(self):
        return (self.end_time, self.end_range)

    def set_end(self, end_time, end_range):
        self.end_time, self.end_range = end_time, end_range

    def __str__(self):
        return "<Sequence: Start " + self.start_time + " End " +\
                self.end_time + " Pin " + str(self.pin) + ">"

class Pin(object):

    def __init__(self, number, sequences=None, name=None, state=0, prio=0):
        ''' State = 0 -> Undef | 1 -> ON | -1 -> OFF
        '''
        self.number = number
        self.prio = prio
        self.sequences = sequences if sequences else []
        for sequence in self.sequences:
            sequence.set_pin(self)

        self.state = state
        self.id = number
        if name is None:
            self.name = "Pin {0}".format(number)
        else:
            self.name = name

    def get_sequences(self):
        return self.sequences

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        if (new_state in [SWITCH_ON, SWITCH_OFF, SWITCH_UNDEF]):
            self.state = new_state
        else:
            raise ValueError("Pin state not valide.")

    def get_id(self):
        return self.number

    def set_id(self, pin_id):
        self.id = pin_id
 
    def get_prio(self):
        return self.prio

    def set_prio(self, prio):
        self.prio = prio
