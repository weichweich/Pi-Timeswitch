# -*- coding: utf-8 -*-
"""This module provides adapters which takes setters, getters and delete
functions. The adapter itself provides GET, POST, PATCH and DELETE functions
which takes or provides JSONAPI encoded objects.
"""

import logging

from flask import request
from flask_restful import Resource

from marshmallow_jsonapi.exceptions import IncorrectTypeError
from marshmallow import ValidationError

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)

# ######################################
# # Single Resource:
# ######################################

class SingleResource(Resource):
    """This class provides functions for GET, POST, DELETE and PATCH methods.
    It seralizes and deseralizes objects using the given schema.

    :param Schema schema: A schema to seralize and deseralize objects
    :param Callable getter_func: function to retrieve objects
    :param Callable setter_func: function to save objects
    :param Callable delete_func: function to delete objects
    :param list decorators: decorator for all methods
    """

    method_decorators = []
    def __init__(self, schema, getter_func=None, setter_func=None, delete_func=None, decorators=None):
        self.getter_func = getter_func
        self.setter_func = setter_func
        self.delete_func = delete_func
        self.schema_many = schema(many=True)
        self.schema_single = schema(many=False)
        if decorators:
            self.method_decorators = decorators

    def get(self, *args, **kwargs):
        """Passes args and kwargs to the getter function, retrieves a object and
        returns the seralized object.
        """
        if not self.getter_func:
            return "Methode not allowed!", 405

        recource = self.getter_func(*args, **kwargs)
        result = self.schema_single.dump(recource)
        return result.data, 200

    def post(self, *args, **kwargs):
        """Deseralizes the request body and passes the retrieved object to the
        setter function. Also passes all args and kwargs to the setter function.

        :return: tupel of added object as json string and http status code
        :rtype: (str, int)
        """
        if not self.setter_func:
            return "Methode not allowed!", 405

        request_json = request.get_json(force=True)
        try:
            self.schema_single.validate(request_json)
        except ValidationError as err:
            LOGGER.warning("ValidationError POST \n\t"\
                + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400
        except IncorrectTypeError as err:
            LOGGER.warning("IncorrectTypeError POST \n\t"\
             + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400

        result = self.schema_single.load(request_json)
        added_item = result.data
        self.setter_func(added_item, *args, **kwargs)
        added_item_json = self.schema_single.dump(added_item)
        return added_item_json.data, 201

    def delete(self, *args, **kwargs):
        """Passes args and kwargs to the delete function.

        :return: String and HTTP status code
        :rtype: (str, int)
        """
        if not self.delete_func:
            return "Methode not allowed!", 405

        self.delete_func(*args, **kwargs)
        return "", 204

    def patch(self, *args, **kwargs):
        """Deseralizes the request body and passes the deseralizes object to the
        setter function. Also passes args and kwargs to the setter function.

        :return: tupel of JSONAPI encoded patched object and HTTP status code
        :rtype: (str, int)
        """
        if not self.setter_func:
            return "Methode not allowed!", 405

        request_json = request.get_json(force=True)
        try:
            self.schema_single.validate(request_json)
        except ValidationError as err:
            LOGGER.warning("ValidationError PATCH \n"\
                + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400
        except IncorrectTypeError as err:
            LOGGER.warning("IncorrectTypeError PATCH \n"\
             + str(err.messages) + "\n" + str(request_json))
            return err.messages, 400

        result = self.schema_single.load(request_json)
        added_item = result.data
        new_item = self.setter_func(added_item, *args, **kwargs)
        new_item_json = self.schema_single.dump(new_item)
        return new_item_json.data, 200

# ######################################
# # Many Resource:
# ######################################

class ManyRessource(SingleResource):
    """This class provides functions for GET, POST, DELETE and PATCH methods.
    It seralizes and deseralizes objects using the given schema.

    :param schema: A schema to seralize and deseralize objects
    :type schema: Schema
    :param getter_func: function to retrieve objects
    :type getter_func: Callable
    :param setter_func: function to save objects
    :type setter_func: Callable
    :param delete_func: function to delete objects
    :type delete_func: Callable
    :param decorators: decorator for all methods
    :type decorators: list
    """

    def get(self, *args, **kwargs):
        """Passes args and kwargs to the getter function, retrieves all objects
        and returns the seralized objects.

        :return: tupel of JSONAPI encoded objects and HTTP status code
        :rtype: (str, int)
        """
        if not self.getter_func:
            return "Methode not allowed!", 405

        resource = self.getter_func(*args, **kwargs)
        result = self.schema_many.dump(resource)
        return result.data, 200

    def delete(self, *args, **kwargs):
        """DELETE method not implemented for multiple objects.
        """
        if not self.delete_func:
            return "Methode not allowed!", 405
        return "Not Implemented", 501

    def patch(self, *args, **kwargs):
        """PATCH method not implemented for multiple objects.
        """
        if not self.setter_func:
            return "Methode not allowed!", 405
        return "Not Implemented", 501
