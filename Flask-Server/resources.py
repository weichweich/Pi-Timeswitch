#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource
from time_switch.model import Sequence, Pin, is_absolute_time, is_relative_time

from schema import SequenceSchema, PinSchema
from marshmallow_jsonapi.exceptions import IncorrectTypeError
from marshmallow import ValidationError

import logging

import time

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)


PIN_SCHEMA = PinSchema(many=False)
PINS_SCHEMA = PinSchema(many=True)
SEQUENCE_SCHEMA = SequenceSchema(many=False)
SEQUENCES_SCHEMA = SequenceSchema(many=True)

class PinsResource(Resource):
    '''Specifies the REST API for accessing pins.'''

    def __init__(self, switch_manager):
        self.switch_manager = switch_manager

    def get(self):
        '''Handels a GET message.'''
        switch_model = self.switch_manager.get_model()
        pins = switch_model.get_pins()
        result = PINS_SCHEMA.dump(pins)
        return result.data, 200

    def post(self):
        '''Handels a POST message.'''
        switch_model = self.switch_manager.get_model()
        request_json = request.get_json(force=True)

        try:
            PIN_SCHEMA.validate(request_json)
        except ValidationError as err:
            LOGGER.warn("ValidationError POST /pins \n"\
                + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400
        except IncorrectTypeError as err:
            LOGGER.warn("IncorrectTypeError POST /pins \n"\
             + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400

        result = PIN_SCHEMA.load(request_json)
        switch_model.set_pin(result.data)
        return "", 200

class PinResource(Resource):
    '''Specifies the REST API for accessing a single pin.'''

    def __init__(self, switch_manager):
        self.switch_manager = switch_manager

    def get(self, pin_id):
        '''Handels a GET message.'''
        switch_model = self.switch_manager.get_model()
        pins = switch_model.get_pin(pin_id)

        result = PIN_SCHEMA.dump(pins)
        return result.data, 200

    def delete(self, pin_id):
        switch_model = self.switch_manager.get_model()

        switch_model.delete_pin(pin_id)
        return "", 204

    def patch(self, pin_id):
        switch_model = self.switch_manager.get_model()
        request_json = request.get_json(force=True)

        try:
            PIN_SCHEMA.validate(request_json)
        except ValidationError as err:
            LOGGER.warn("ValidationError PATCH /pin \n"\
                + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400
        except IncorrectTypeError as err:
            LOGGER.warn("IncorrectTypeError PATCH /pin \n"\
             + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400

        pin = PIN_SCHEMA.load(request_json)
        switch_model.set_pin(pin.data)

        return "", 204

    def put(self, pin_id):
        '''Handels a PUT message.'''
        switch_model = self.switch_manager.get_model()
        request_json = request.get_json(force=True)

        try:
            PIN_SCHEMA.validate(request_json)
        except ValidationError as err:
            LOGGER.warn("ValidationError PUT /pin \n"\
                + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400
        except IncorrectTypeError as err:
            LOGGER.warn("IncorrectTypeError PUT /pin \n"\
             + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400

        pin = PIN_SCHEMA.load(request_json)
        switch_model.set_pin(pin.data)

        return "", 204

class SequencesResource(Resource):
    '''Specifies the REST API for accessing sequences'''
    def __init__(self, switch_manager):
        self.switch_manager = switch_manager
        self.sequence_schema = SequenceSchema()

    def get(self):
        '''Handels a GET message.'''
        switch_model = self.switch_manager.get_model()
        sequences = switch_model.get_sequences()
        result = SEQUENCES_SCHEMA.dump(sequences)
        return result.data

    def post(self):
        '''Handels a POST message.'''
        switch_model = self.switch_manager.get_model()
        request_json = request.get_json(force=True)
        load_result = SEQUENCE_SCHEMA.load(request_json)

        sequence = load_result.data

        switch_model.set_sequence(sequence)

        sequences = switch_model.get_sequences()
        result = SEQUENCES_SCHEMA.dump(sequences)
        return result.data

class SequenceResource(Resource):
    '''Specifies the REST API for accessing sequences'''

    def __init__(self, switch_manager):
        self.switch_manager = switch_manager
        self.sequence_schema = SequenceSchema()

    def get(self, sequence_id):
        '''Handels a GET message.'''
        switch_model = self.switch_manager.get_model()
        sequences = switch_model.get_sequence(sequence_id)
        result = SEQUENCE_SCHEMA.dump(sequences)
        return result.data

    def post(self, sequence_id):
        '''Handels a POST message.'''
        switch_model = self.switch_manager.get_model()
        request_json = request.get_json(force=True)
        load_result = SEQUENCE_SCHEMA.load(request_json)

        sequence = load_result.data

        sequence.set_id(sequence_id)
        switch_model.set_sequence(sequence)

        sequences = switch_model.get_sequences()
        result = SEQUENCES_SCHEMA.dump(sequences)
        return result.data

    def delete(self, sequence_id):
        '''Handels a DELETE message.'''
        switch_model = self.switch_manager.get_model()
        switch_model.delete_sequence(sequence_id)
        
        sequences = switch_model.get_sequences()
        result = SEQUENCES_SCHEMA.dump(sequences)
        return result.data
 
