#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource
from time_switch.model import Sequence, Pin, is_absolute_time, is_relative_time

from marshmallow import ValidationError, fields, post_load, validates_schema
from marshmallow_jsonapi import Schema
from marshmallow_jsonapi.exceptions import IncorrectTypeError
import logging

import time

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
    id = fields.Str(dump_only=True)

    pin_id = fields.Integer(required={'message': 'Foreign key pin id is required!', 'code': 400})

    start_time = fields.String(required=True)
    start_range = fields.String(required=True)
    end_time = fields.String(required=True)
    end_range = fields.String(required=True)

    @post_load
    def make_sequence(self, data):
        return Sequence(**data)

    def handle_error(self, exc, data):
        raise ValidationError('An error occurred with input: {0} \n {1}'.format(data, exc.messages))

    class Meta:
        type_ = 'sequences'
        inflect = dasherize

class PinSchema(Schema):
    id = fields.Str(dump_only=True)
    pin_num = fields.Integer(required=True)
    name = fields.String(attribute='name')
    state = fields.Integer()

    @post_load
    def make_pin(self, data):
        return Pin(**data)

    def handle_error(self, exc, data):
        raise ValidationError('An error occurred with input: {0} \n {1}'.format(data, exc.messages))

    class Meta:
        type_ = 'pins'
        inflect = dasherize
