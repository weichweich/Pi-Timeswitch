#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource
from time_switch.model import Sequence, Pin, is_absolute_time, is_relative_time

from marshmallow import Schema, ValidationError, fields, post_load, validates_schema

import logging

import time

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)

# ######################################
# # Schema:
# ######################################

class AppError(Exception):
    pass

class SequenceSchema(Schema):
    id = fields.Integer(attribute='sequence_id', load_from='id', required=False)
    pin = fields.Integer(load_from='pin', attribute='pin_id',
                         required={'message': 'Foreign key pin id is required!', 'code': 400})

    fromTm = fields.String(attribute='start_tm', load_from='fromTm', required=True)
    fromRange = fields.String(attribute='start_range', load_from='fromRange', required=True)
    toTm = fields.String(attribute='end_tm', load_from='toTm', required=True)
    toRange = fields.String(attribute='end_range', load_from='toRange', required=True)

    @post_load
    def make_sequence(self, data):
        return Sequence(**data)

    @validates_schema
    def validate_numbers(self, data):
        if not is_relative_time(data['start_range']):
            raise ValidationError('field_a must be greater than field_b')
        elif not is_relative_time(data['end_range']):
            raise ValidationError('field_a must be greater than field_b')
        elif not (is_relative_time(data['end_tm']) or is_absolute_time(data['end_tm'])):
            raise ValidationError('End time must be HH:MM or an integer in range [0, 1440]')
        elif not (is_relative_time(data['start_tm']) or is_absolute_time(data['start_tm'])):
            raise ValidationError('Start time must be HH:MM or an integer in range [0, 1440]')
        elif is_relative_time(data['start_tm']) and is_relative_time(data['end_tm']):
            raise ValidationError('Either start or end time can be relativ but not both.')

    def handle_error(self, exc, data):
        LOGGER.error(exc.messages)
        raise AppError('An error occurred with input: {0}'.format(data))

class PinSchema(Schema):
    id = fields.Integer(attribute='pin_id', load_from='id', required=True)
    name = fields.String(attribute='name')

    @post_load
    def make_pin(self, data):
        return Pin(**data)

    def handle_error(self, exc, data):
        LOGGER.error(exc.messages)
        raise AppError('An error occurred with input: {0}'.format(data))

# ######################################
# # Resources:
# ######################################

PIN_SCHEMA = PinSchema(many=False)
PINS_SCHEMA = PinSchema(many=True)
SEQUENCE_SCHEMA = SequenceSchema(many=False)
SEQUENCES_SCHEMA = SequenceSchema(many=True)

class SwitchResource(Resource):
    '''Specifies the REST API for switching pins on and off.'''

    def __init__(self, switch_manager):
        self.switch_manager = switch_manager

    def post(self):
        '''Handels a POST message.'''
        return "", 201

class PinsResource(Resource):
    '''Specifies the REST API for accessing pins.'''

    def __init__(self, switch_manager):
        self.switch_manager = switch_manager

    def get(self):
        '''Handels a GET message.'''
        switch_model = self.switch_manager.get_model()
        pins = switch_model.get_pins()
        result = PINS_SCHEMA.dump(pins)
        return {'pins':result.data}

    def post(self):
        '''Handels a POST message.'''
        switch_model = self.switch_manager.get_model()
        request_json = request.get_json(force=True)
        result = PIN_SCHEMA.load(request_json['pin'])

        switch_model.set_pin(result.data)
        return self.get(), 201

class PinResource(Resource):
    '''Specifies the REST API for accessing pins.'''

    def __init__(self, switch_manager):
        self.switch_manager = switch_manager

    def get(self, pin_id):
        '''Handels a GET message.'''
        switch_model = self.switch_manager.get_model()
        pins = switch_model.get_pin(pin_id)

        result = PIN_SCHEMA.dump(pins)
        return {'pins':result.data}

    def put(self, pin_id):
        '''Handels a POST message.'''
        switch_model = self.switch_manager.get_model()
        request_json = request.get_json(force=True)
        pin = PIN_SCHEMA.load(request_json['pin'])
        pin.data.set_id(pin_id)
        switch_model.set_pin(pin.data)

        pins = switch_model.get_pin(pin_id)
        result = PIN_SCHEMA.dump(pins)
        return {'pins':result.data}

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
        return {'schedules':result.data}

    def post(self):
        '''Handels a POST message.'''
        switch_model = self.switch_manager.get_model()
        request_json = request.get_json(force=True)
        load_result = SEQUENCE_SCHEMA.load(request_json['schedule'])

        sequence = load_result.data

        switch_model.set_sequence(sequence)

        sequences = switch_model.get_sequences()
        result = SEQUENCES_SCHEMA.dump(sequences)
        return {'schedules':result.data}

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
        return {'schedules':result.data}

    def post(self, sequence_id):
        '''Handels a POST message.'''
        switch_model = self.switch_manager.get_model()
        request_json = request.get_json(force=True)
        load_result = SEQUENCE_SCHEMA.load(request_json['schedule'])

        sequence = load_result.data

        sequence.set_id(sequence_id)
        switch_model.set_sequence(sequence)

        sequences = switch_model.get_sequences()
        result = SEQUENCES_SCHEMA.dump(sequences)
        return {'schedules':result.data}

    def delete(self, sequence_id):
        '''Handels a DELETE message.'''
        switch_model = self.switch_manager.get_model()
        switch_model.delete_sequence(sequence_id)
        
        sequences = switch_model.get_sequences()
        result = SEQUENCES_SCHEMA.dump(sequences)
        return {'schedules':result.data}
 
