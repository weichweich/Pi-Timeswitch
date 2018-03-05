import os
from functools import wraps

import pytest
from flask import url_for

import timeswitch
from timeswitch.server import app_setup, create_db, prepare_app


def dummy_auth(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return func_wrapper


class Args(object):
    static_dir=None
    schedule_file="testing.db"


@pytest.fixture
def app():
    timeswitch.auth.dec_auth = dummy_auth

    app = prepare_app(Args())
    app.testing = True
    create_db(app)
    switch_model = app_setup(app)

    yield app.test_client()

    os.remove(Args.schedule_file)
