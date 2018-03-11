import argparse
import logging
import sys

from timeswitch.switch.manager import SwitchManager
from timeswitch.app import setup_app
from timeswitch.api import setup_api
from timeswitch.model import setup_model

# ######################################
# # parsing commandline args
# ######################################
def parse_arguments():
    PARSER = argparse.ArgumentParser(description='Timeswitch for the\
     GPIOs of an Raspberry Pi with a webinterface.')

    PARSER.add_argument('-f', '--file', dest='schedule_file', metavar='file',
                        type=str, required=True,
                        help='A JSON-file containing the schedule.')

    PARSER.add_argument('--debug', action='store_true',
                        help='A JSON-file containing the schedule.')

    PARSER.add_argument('--create', dest='create', action='store_true',
                        help='Creates a new database. DELETES ALL DATA!!')

    PARSER.add_argument('--manager', dest='manager', action='store_true',
                        help='Start the manager which switches the GPIOs at specified times.')

    PARSER.add_argument('--static', dest='static_dir', metavar='file',
                        type=str, help='Folder with static files to serve')

    return PARSER.parse_args()

# ######################################
# # Logging:
# ######################################

def get_logger(cmd_args):
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-20s \
                        %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='piSwitch.log',
                        filemode='a')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()

    if cmd_args.debug:
        console.setLevel(logging.DEBUG)
    else:
        console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(levelname)-8s:%(name)-8s:%(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    return logging.getLogger("MAIN")


def start(cmd_args, app, switch_model):
    switch_manager = None
    if cmd_args.manager:
        switch_manager = SwitchManager(switch_model)
        switch_manager.start()

    try:
        app.run(debug=cmd_args.debug)
    finally:
        if cmd_args.manager:
            switch_manager.stop()


def main():
    cmd_args = parse_arguments()
    app = setup_app(cmd_args)
    model = setup_model(app)
    api = setup_api(app, model)

    start(cmd_args, app, model)


if __name__ == '__main__':
    main()
