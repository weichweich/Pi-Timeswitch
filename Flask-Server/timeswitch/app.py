from flask import Flask

def setup_app(*args, **kwargs):
    app = Flask(__name__, *args, **kwargs)
    app.config.from_object("timeswitch.config.Config")
    app.config.from_envvar('TIMESWITCH_SETTINGS', silent=True)
    return app
