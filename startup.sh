#!/bin/bash

set -x

BASEDIR="/home/pi/dist/backend/"
VENV="/home/pi/"
DATABASE=$VENV"TimeswitchData/schedule.sqlite"

sudo $VENV"venv/bin/uwsgi" --stop /tmp/timeswitch.pid
sudo $VENV"venv/bin/uwsgi" --ini $BASEDIR"timeswitch.ini" --pyargv "--file "$DATABASE
screen -dmS "timeswitch"  sh -c 'sudo $VENV"venv/bin/timer" $BASEDIR"timer.py" --file $DATABASE |tee "/home/pi/timer.log"'
