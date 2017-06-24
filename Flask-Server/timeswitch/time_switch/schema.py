# -*- coding: utf-8 -*-

import logging
import time

from flask import request
from flask_restful import Resource
from time_switch.model import Sequence, Pin, is_absolute_time, is_relative_time

from marshmallow import ValidationError, post_load, validates_schema
from marshmallow_jsonapi import Schema, fields

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)

class AppError(Exception):
    pass

def dasherize(text):
    return text.replace('_', '-')

class SequenceSchema(Schema):
    id = fields.String(dump_only=True)

    start_time = fields.String(required=True)
    start_range = fields.String(required=True)
    end_time = fields.String(required=True)
    end_range = fields.String(required=True)
    pin = fields.Relationship(
        related_url='/api/pins/{pin_id}',
        related_url_kwargs={'pin_id': '<pin>'},
        # Include resource linkage
        many=False, include_data=True,
        type_='pins'
    )

    @post_load
    def make_sequence(self, data):
        return Sequence(**data)

    def handle_error(self, exc, data):
        raise ValidationError('An error occurred with input: {0} \n {1}'.format(data, exc.messages))

    def __str__(self):
        if self.pin is None:
            return "<Sequence: Start " + self.start_time + " End " +\
                    self.end_time + " Pin none>"
        else:
            return "<Sequence: Start " + self.start_time + " End " +\
                    self.end_time + " Pin " + str(self.pin) + ">"

    class Meta:
        type_ = 'sequences'
        strict = True

class PinSchema(Schema):
    id = fields.Str(dump_only=True)
    number = fields.Integer(required=True)
    name = fields.String(attribute='name')
    state = fields.Integer()
    sequences = fields.Relationship(
        related_url='/api/pins/{pin_id}/sequences',
        related_url_kwargs={'pin_id': '<id>'},
        # Include resource linkage
        many=True,
        include_data=True,
        type_='sequences',
        schema='SequenceSchema'
    )

    @post_load
    def make_pin(self, data):
        return Pin(**data)

    def handle_error(self, exc, data):
        raise ValidationError('An error occurred with input: {0} \n {1}'.format(data, exc.messages))

    class Meta:
        type_ = 'pins'
        strict = True
