import os
import unittest
import tempfile

import timeswitch.server

import tests.helper


def test_prepare_app():
    cmd_args = tests.helper.Bunch(static_dir="",
                                  schedule_file="schedule.sqlite",
                                  create=True)
    app = timeswitch.server.prepare_app(cmd_args)

    assert app

def test_app_setup():
    cmd_args = tests.helper.Bunch(static_dir="",
                                  schedule_file="schedule.sqlite",
                                  create=True)
    app = timeswitch.server.prepare_app(cmd_args)
    assert app
    timeswitch.server.create_db(app)

    switch_model = timeswitch.server.app_setup(app)
    assert switch_model
