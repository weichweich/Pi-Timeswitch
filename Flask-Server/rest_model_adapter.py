# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource

from marshmallow_jsonapi.exceptions import IncorrectTypeError
from marshmallow import ValidationError

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)

# ######################################
# # Single Resource:
# ######################################

class SingleResource(Resource):
    method_decorators = []
    def __init__(self, schema, getter_func=None, setter_func=None, delete_func=None, decorators=[]):
        self.getter_func = getter_func
        self.setter_func = setter_func
        self.delete_func = delete_func
        self.schemaSingle = schema(many=True)
        self.schemaSingle = schema(many=False)
        self.method_decorators = decorators

    def get(self, *args, **kwargs):
        '''Handels a GET message.'''
        if not self.getter_func:
            return "Methode not allowed!", 405

        recource = self.getter_func(*args, **kwargs)
        result = self.schemaSingle.dump(recource)
        return result.data, 200

    def post(self, *args, **kwargs):
        '''Handels a POST message.'''
        if not self.setter_func:
            return "Methode not allowed!", 405

        request_json = request.get_json(force=True)
        try:
            self.schemaSingle.validate(request_json)
        except ValidationError as err:
            LOGGER.warn("ValidationError POST \n\t"\
                + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400
        except IncorrectTypeError as err:
            LOGGER.warn("IncorrectTypeError POST \n\t"\
             + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400

        result = self.schemaSingle.load(request_json)
        self.setter_func(result.data, *args, **kwargs)
        return "", 200

    def delete(self, *args, **kwargs):
        if not self.delete_func:
            return "Methode not allowed!", 405

        self.delete_func(*args, **kwargs)
        return "", 204

    def patch(self, *args, **kwargs):
        if not self.setter_func:
            return "Methode not allowed!", 405

        request_json = request.get_json(force=True)
        try:
            self.schemaSingle.validate(request_json)
        except ValidationError as err:
            LOGGER.warn("ValidationError PATCH \n"\
                + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400
        except IncorrectTypeError as err:
            LOGGER.warn("IncorrectTypeError PATCH \n"\
             + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400

        result = self.schemaSingle.load(request_json)
        self.setter_func(result.data, *args, **kwargs)
        return "", 204

# ######################################
# # Many Resource:
# ######################################

class ManyRessource(Resource):
    def __init__(self, schema, getter_func=None, setter_func=None, delete_func=None, decorators=None):
        self.getter_func = getter_func
        self.setter_func = setter_func
        self.delete_func = delete_func
        self.schemaMany = schema(many=True)
        self.schemaSingle = schema(many=False)

    def get(self, *args, **kwargs):
        '''Handels a GET message.'''
        if not self.getter_func:
            return "Methode not allowed!", 405

        resource = self.getter_func(*args, **kwargs)
        result = self.schemaMany.dump(resource)
        return result.data, 200

    def post(self, *args, **kwargs):
        '''Handels a POST message.'''
        if not self.setter_func:
            return "Methode not allowed!", 405

        request_json = request.get_json(force=True)
        try:
            self.schemaSingle.validate(request_json)
        except ValidationError as err:
            LOGGER.warn("ValidationError POST \n"\
                + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400
        except IncorrectTypeError as err:
            LOGGER.warn("IncorrectTypeError POST \n"\
             + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400

        result = self.schemaSingle.load(request_json)
        self.setter_func(result.data, *args, **kwargs)
        return request_json, 201

    def delete(self, *args, **kwargs):
        if not self.delete_func:
            return "Methode not allowed!", 405
        return "Not Implemented", 501

    def patch(self, *args, **kwargs):
        if not self.setter_func:
            return "Methode not allowed!", 405
        return "Not Implemented", 501
