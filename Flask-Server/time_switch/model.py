# -*- coding: utf-8 -*-

import sqlite3 as sql
import logging
import time
import os

from flask import current_app

from time_switch.dao import Pin, Sequence, SWITCH_ON, SWITCH_OFF, SWITCH_UNDEF

class NullHandler(logging.Handler):
	def emit(self, record):
		pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)

try:
	import RPi.GPIO as GPIO
except ImportError:
	import time_switch.no_gpio as GPIO
possible_gpios = [2, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24,
				  26, 29, 31, 32, 33, 35, 36, 37, 38, 40]

### Helper methodes
## create db
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
			name TEXT)''')

## validate data

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

### MODEL ###
PRIO_KEY = 'prio'
STATE_KEY = 'state'

class PiSwitchModel(object):
	'''This class saves and loads pins and schedules.'''

	def __init__(self, filename):
		self.sql_file = filename
		self.observers = []
		self.pin_info = {}
		GPIO.setmode(GPIO.BOARD)

		try:
			self.get_pins()
		except:
			create_db(filename)

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
			return sequences

	def get_sequence(self, sequence_id):
		'''Returns all schedules in the dataset.'''

		LOGGER.info("get_sequence({0})".format(sequence_id))

		with sql.connect(self.sql_file) as connection:
			cur = connection.cursor()
			cur.execute('''SELECT * FROM Sequences
						WHERE id=?''', (sequence_id,))

			row = cur.fetchone()
			pin = self.__get_pin_for_sequence(sequence_id)

			if row is None:
				return None
			elif pin is None:
				print("none?")
				return None
			else:
				sequence = get_sequence_from_row(row)
				sequence.set_pin(pin)
				return sequence

	def set_sequence(self, sequence, pin_id=-1):
		'''Adds the given sequence to the dataset.\
		   Removes the old schedule if it exists.'''
		with sql.connect(self.sql_file) as connection:
			cur = connection.cursor()
			if sequence.get_pin() and pin_id==-1:
				pin_id = sequence.get_pin().get_id()

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
				LOGGER.info("set_sequence({0}) - updating sequence"\
					.format(sequence.get_id()))
				vals = (sequence.sequence_id, pin_id,
						sequence.get_start()[0], sequence.get_start()[1],
						sequence.get_end()[0], sequence.get_end()[1])
				cur.execute('''REPLACE INTO
							Sequences(id, pin_id, start_time, start_range,\
							end_time, end_range)
							VALUES (?, ?, ?, ?, ?, ?)''', vals)
		return self.get_sequence(sequence.get_id())

	def delete_sequence(self, sequence_id):
		'''Deletes the sequences with the given id.'''
		with sql.connect(self.sql_file) as connection:
			cur = connection.cursor()
			cur.execute('''DELETE FROM Sequences
						WHERE id=?''', (sequence_id,))

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
				sequences.append(Sequence(start_time, start_range, end_time,
								  end_range, sequence_id=sequence_id, pin=pin))
			return sequences


	def __get_pin_for_sequence(self, sequence_id):
		'''Returns all sequences for the pin.'''
		with sql.connect(self.sql_file) as connection:
			cur = connection.cursor()
			cur.execute('''SELECT Pins.id, Pins.name FROM pins
				JOIN Sequences
				ON Sequences.pin_id = Pins.id
				WHERE Sequences.id =?''', (str(sequence_id),))

			row = cur.fetchone()
			if row is None:
				return None

			return Pin(row[0], None, row[1])

	def __delete_sequences_for_pin(self, pin_id):
		'''Deletes all sequences for the pin.'''
		with sql.connect(self.sql_file) as connection:
			cur = connection.cursor()
			cur.execute('''DELETE FROM Sequences
				WHERE pin_id=?''', (str(pin_id),))

			rows = cur.fetchall()

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
				pins.append(Pin(row[0], sequences, row[1]))

			return pins

	def get_pin(self, pin_id):
		'''Returns the pin with the given id.'''
		with sql.connect(self.sql_file) as connection:
			cur = connection.cursor()
			cur.execute('''SELECT * FROM Pins
				WHERE id=?''', (str(pin_id),))

			row = cur.fetchone()
			if row is None:
				return None

			sequences = self.get_sequences_for_pin(pin_id)
			rawPin = row
			return Pin(rawPin[0], sequences, rawPin[1])

	def delete_pin(self, pin_id):
		'''Deletes all sequence for the pin and the pin it selfs.'''
		self.__delete_sequences_for_pin(pin_id)
		GPIO.cleanup(pin_id)

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

		with sql.connect(self.sql_file) as connection:
			cur = connection.cursor()
			cur.execute('''REPLACE INTO Pins(id, name)
						VALUES (?, ?)''',
						(pin.get_id(), pin.get_name()))

			if pin.get_sequences() is not None:
				for sequence in pin.get_sequences():
					self.set_sequence(sequence)
		return self.get_pin(pin.get_id())

	def switch_pin_on(self, pin, prio=0):
		if not pin.get_id() in self.pin_info:
			self.__setup_info(pin)

		self.__switch_state(pin, SWITCH_ON, prio)

	def switch_pin_off(self, pin, prio=0):
		if not pin.get_id() in self.pin_info:
			self.__setup_info(pin)

		self.__switch_state(pin, SWITCH_OFF, prio)

	def __setup_info(self, pin):
		self.pin_info[pin.get_id()] = {
			STATE_KEY: SWITCH_UNDEF,
			PRIO_KEY: 0
		}
		GPIO.setup(pin.get_id(), GPIO.OUT)

	def __switch_state(self, pin, state, prio):
		info = self.pin_info[pin.get_id()]
		if not info[PRIO_KEY]:
			info[PRIO_KEY] = prio

		if info[STATE_KEY] != state and info[PRIO_KEY] <= prio:
			LOGGER.info(u"Switch State: {0} Id: {1:2} Name: {2} Prio: {3}"
				.format(state, pin.get_id(), pin.get_name(), prio))
			pin.set_state(state)
			info[STATE_KEY] = state
			if state == SWITCH_ON:
				GPIO.output(pin.get_id(), GPIO.HIGH)
			elif state == SWITCH_OFF:
				GPIO.output(pin.get_id(), GPIO.LOW)

		elif info[STATE_KEY] == state:
			info[PRIO_KEY] = prio
		else:
			LOGGER.info(u"No switching done. Current prio:{0} - order prio:{1}"
				.format(info[PRIO_KEY], prio))

	def cleanup_all_pins(self):
		GPIO.cleanup()
