import os
from functools import wraps

import pytest
from flask import url_for

import timeswitch
from timeswitch.app import setup_app
from timeswitch.api import setup_api
from timeswitch.model import setup_model


def dummy_auth(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return func_wrapper


@pytest.fixture
def app(tmpdir):
    timeswitch.auth.dec_auth = dummy_auth

    app = setup_app()
    app.testing = True
    app.config['DB_FILE'] = tmpdir.join('test.db').strpath
    model = None
    with app.app_context():
        model = setup_model(app)
    
    _ = setup_api(app, model)

    yield app.test_client()
