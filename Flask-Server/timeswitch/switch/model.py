# -*- coding: utf-8 -*-

import logging
import sqlite3 as sql
import time

from flask import current_app

from timeswitch.switch.dao import (SWITCH_OFF, SWITCH_ON, SWITCH_UNDEF, Pin,
                                   Sequence)

try:
    import RPi.GPIO as GPIO
except ImportError:
    import timeswitch.switch.no_gpio as GPIO


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)


possible_gpios = [2, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24,
                  26, 29, 31, 32, 33, 35, 36, 37, 38, 40]

# Helper methodes
# create db


def create_db():
    '''Creates all tables.'''
    with sql.connect(current_app.config['SQL_FILE']) as connection:
        cur = connection.cursor()
        cur.execute('''CREATE TABLE Sequences(
            id INTEGER PRIMARY KEY,
            pin_id INTEGER,
            start_time TEXT,
            start_range TEXT,
            end_time TEXT,
            end_range TEXT,
            FOREIGN KEY(pin_id) REFERENCES Pins(id) ON UPDATE CASCADE)''')
        cur.execute('''CREATE TABLE Pins(
            id INTEGER PRIMARY KEY,
            prio INTEGER,
            name TEXT)''')
    connection.close()

# validate data


def is_absolute_time(check_time):
    try:
        time.strptime(check_time, '%H:%M')
        return True
    except ValueError:
        return False


def is_relative_time(check_time):
    try:
        as_int = int(check_time)
        return 0 <= as_int and as_int <= 1440
    except ValueError:
        return False
    except TypeError:
        return False


def get_sequence_from_row(row):
    (sequence_id, pin_id, start_time, start_range, end_time, end_range) = row
    return Sequence(start_time, start_range, end_time,
                    end_range, sequence_id=sequence_id)


def get_sequences_from_rows(rows):
    sequences = []
    for (sequence_id, pin_id, start_time, start_range, end_time, end_range) in rows:
        sequences.append(Sequence(start_time, start_range, end_time,
                                  end_range, sequence_id=sequence_id))

    return sequences


class SwitchModel(object):
    '''This class saves and loads pins and schedules.'''

    def __init__(self, filename):
        self.sql_file = filename
        self.observers = []
        self.used_gpio = {}
        GPIO.setmode(GPIO.BOARD)

        try:
            self.get_pins()
        except:
            create_db()

    def __notify_all(self):
        for observer in self.observers:
            observer.changed()

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def get_sequences(self):
        '''Returns all schedules in the dataset.'''
        sequences = []
        with sql.connect(self.sql_file) as connection:
            cur = connection.cursor()
            cur.execute("SELECT * FROM Sequences")

            rows = cur.fetchall()

            for (sequence_id, pin_id, start_time,
                 start_range, end_time, end_range) in rows:
                pin = self.__get_pin_for_sequence(sequence_id)
                if pin is None:
                    print("none?")
                sequences.append(Sequence(start_time, start_range, end_time,
                                          end_range, pin=pin, sequence_id=sequence_id))

        connection.close()
        return sequences

    def get_sequence(self, sequence_id):
        '''Returns all schedules in the dataset.'''

        LOGGER.info("get_sequence(%s)", sequence_id)

        with sql.connect(self.sql_file) as connection:
            cur = connection.cursor()
            cur.execute('''SELECT * FROM Sequences
                        WHERE id=?''', (sequence_id,))

            row = cur.fetchone()
            pin = self.__get_pin_for_sequence(sequence_id)
            sequence = None
            if not pin is None:
                sequence = get_sequence_from_row(row)
                sequence.set_pin(pin)
            else:
                LOGGER.error("sequence got no pin!")

        connection.close()
        return sequence

    def set_sequence(self, sequence, pin_id=-1, sequence_id=-1):
        '''Adds the given sequence to the dataset.\
           Removes the old schedule if it exists.'''
        with sql.connect(self.sql_file) as connection:
            cur = connection.cursor()
            if sequence.get_pin() and pin_id == -1:
                pin_id = sequence.get_pin().get_id()

            if sequence.get_id() == -1 and sequence_id != -1:
                sequence.set_id(sequence_id)

            if sequence.get_id() == -1:
                LOGGER.info("set_sequence() - adding new sequence")

                vals = (pin_id, sequence.get_start()[0],
                        sequence.get_start()[1], sequence.get_end()[0],
                        sequence.get_end()[1])

                cur.execute('''INSERT INTO
                            Sequences(pin_id, start_time, start_range,\
                            end_time, end_range)
                            VALUES (?, ?, ?, ?, ?)''', vals)
                sequence.set_id(cur.lastrowid)
            else:
                LOGGER.info("set_sequence(%s) - updating sequence",
                            sequence.get_id())
                vals = (sequence.get_start()[0], sequence.get_start()[1],
                        sequence.get_end()[0], sequence.get_end()[1], sequence.get_id())
                cur.execute('''UPDATE Sequences
                            SET start_time=?, start_range=?, end_time=?, end_range=?
                            WHERE id=?''', vals)
        connection.close()
        return self.get_sequence(sequence.get_id())

    def delete_sequence(self, sequence_id):
        '''Deletes the sequences with the given id.'''
        with sql.connect(self.sql_file) as connection:
            cur = connection.cursor()
            cur.execute('''DELETE FROM Sequences
                        WHERE id=?''', (sequence_id,))
        connection.close()

    def get_sequences_for_pin(self, pin_id):
        '''Returns all sequences for the pin.'''
        with sql.connect(self.sql_file) as connection:
            cur = connection.cursor()
            cur.execute('''SELECT * FROM Sequences
                WHERE pin_id=?''', (str(pin_id),))

            rows = cur.fetchall()

            sequences = []
            for (sequence_id, pin_id, start_time, start_range, end_time, end_range) in rows:
                pin = self.__get_pin_for_sequence(sequence_id)
                seq = Sequence(start_time, start_range, end_time, end_range,
                               sequence_id=sequence_id, pin=pin)
                sequences.append(seq)

        connection.close()
        return sequences

    def __get_pin_for_sequence(self, sequence_id):
        '''Returns all sequences for the pin.'''
        with sql.connect(self.sql_file) as connection:
            cur = connection.cursor()
            cur.execute('''SELECT Pins.id, Pins.prio, Pins.name FROM pins
                JOIN Sequences
                ON Sequences.pin_id = Pins.id
                WHERE Sequences.id =?''', (str(sequence_id),))

            row = cur.fetchone()
            if row is None:
                return None

        connection.close()
        return Pin(row[0], None, row[2], prio=row[1])

    def __delete_sequences_for_pin(self, pin_id):
        '''Deletes all sequences for the pin.'''
        with sql.connect(self.sql_file) as connection:
            cur = connection.cursor()
            cur.execute('''DELETE FROM Sequences
                WHERE pin_id=?''', (str(pin_id),))

            rows = cur.fetchall()

        connection.close()
        return get_sequences_from_rows(rows)

    def get_pins(self):
        '''Returns all pins.'''
        pins = []
        with sql.connect(self.sql_file) as connection:
            cur = connection.cursor()
            cur.execute('''SELECT * FROM Pins''')

            rows = cur.fetchall()

            for row in rows:
                sequences = self.get_sequences_for_pin(row[0])
                raw_pin = row
                pin = Pin(raw_pin[0], sequences, raw_pin[2], prio=raw_pin[1])
                if not pin.get_id() in self.used_gpio:
                    self.__setup_pin(pin)
                pin.set_state(GPIO.input(pin.get_id()))
                pins.append(pin)

        connection.close()
        return pins

    def get_pin(self, pin_id):
        '''Returns the pin with the given id.'''
        with sql.connect(self.sql_file) as connection:
            cur = connection.cursor()
            cur.execute('''SELECT * FROM Pins
                WHERE id=?''', (str(pin_id),))

            raw_pin = cur.fetchone()
            if raw_pin is None:
                return None
        connection.close()

        sequences = self.get_sequences_for_pin(pin_id)
        pin = Pin(raw_pin[0], sequences, raw_pin[2], prio=raw_pin[1])
        if not pin.get_id() in self.used_gpio:
            self.__setup_pin(pin)
        pin.set_state(GPIO.input(pin.get_id()))

        return pin

    def delete_pin(self, pin_id):
        '''Deletes all sequence for the pin and the pin it selfs.'''
        self.__delete_sequences_for_pin(pin_id)
        GPIO.cleanup(pin_id)
        self.used_gpio.pop(pin_id, None)

        with sql.connect(self.sql_file) as connection:
            cur = connection.cursor()
            cur.execute('''DELETE FROM Pins WHERE id=?''',
                        (str(pin_id),))

    def set_pin(self, pin, pin_id=-1):
        '''Alters the pin name or adds the pin if he
        did not exist. Also adds sequences.'''
        if pin.get_state() == SWITCH_ON:
            self.switch_pin_on(pin, prio=1)
        elif pin.get_state() == SWITCH_OFF:
            self.switch_pin_off(pin, prio=1)

        return self.__set_pin(pin, pin_id)

    def __set_pin(self, pin, pin_id=-1):
        '''Alters the pin name or adds the pin if he
        did not exist. Also adds sequences.'''
        if self.get_pin(pin.get_id()) is None:
            with sql.connect(self.sql_file) as connection:
                cur = connection.cursor()
                cur.execute('''INSERT INTO Pins
                            (prio, name, id)
                            VALUES (?,?,?)''',
                            (pin.get_prio(), pin.get_name(), pin.get_id()))
            connection.close()
        else:
            with sql.connect(self.sql_file) as connection:
                cur = connection.cursor()
                cur.execute('''UPDATE Pins
                            SET prio=?, name=?
                            WHERE id=?''',
                            (pin.get_prio(), pin.get_name(), pin.get_id()))
            connection.close()

        if pin.get_sequences() is not None:
            for sequence in pin.get_sequences():
                self.set_sequence(sequence)

        return self.get_pin(pin.get_id())

    def switch_pin_on(self, pin, prio=0):
        self.__switch_state(pin, SWITCH_ON, prio)

    def switch_pin_off(self, pin, prio=0):
        self.__switch_state(pin, SWITCH_OFF, prio)

    def __setup_pin(self, pin):
        pin_id = pin.get_id()
        GPIO.setup(pin_id, GPIO.OUT, initial=GPIO.LOW)
        self.used_gpio[pin_id] = "in use"

    def __switch_state(self, pin, state, prio):
        if not pin.get_id() in self.used_gpio:
            self.__setup_pin(pin)

        old_state = GPIO.input(pin.get_id())
        old_prio = pin.get_prio()

        if old_state != state and old_prio <= prio:
            LOGGER.info("Switch State: {0} Id: {1:2} Name: {2} Prio: {3}"
                        .format(state, pin.get_id(), pin.get_name(), prio))
            pin.set_state(state)
            if state == SWITCH_ON:
                GPIO.output(pin.get_id(), GPIO.HIGH)
            elif state == SWITCH_OFF:
                GPIO.output(pin.get_id(), GPIO.LOW)

        elif old_state == state:
            pin.set_prio(prio)
            self.__set_pin(pin)
        else:
            LOGGER.info("No switching done.")

    def cleanup_all_pins(self):
        GPIO.cleanup()
        self.used_gpio = {}
