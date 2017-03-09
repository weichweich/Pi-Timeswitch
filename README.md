# Pi-TimeSwitch
Pi-TimeSwitch is an automated, easy to use timeswitch for the [Raspberry Pi](https://www.raspberrypi.org).

Pi-TimeSwitch provides a web based GUI where one can specify a schedule for every gpio. Start and end time of each intervall can be randomized.

Currently the project is in an **early state of development**. There are several **bugs** in the GUI and some features are missing.

## How to install Pi-TimeSwitch:

Ensure that pip is installed:

~~~
sudo easy_install pip
~~~

### Virtualenv

At first i recommend to create a virtual environment using [Virtualenv](https://virtualenv.pypa.io/en/stable/).

Install Virtualenv:

~~~
pip install virtualenv
~~~

Create a virtual environment:

~~~
cd pi-timeswitch-folder
virtualenv venv
~~~
Activate it:

~~~
source venv/bin/activate
~~~

### Prepare Flask-Backend

Then you need to install [Flask](http://flask.pocoo.org), [Flask-Restful](http://flask-restful.readthedocs.org/en/0.3.4/), [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO), [marshmallow](http://marshmallow.readthedocs.org/en/latest/), [marshmallow-jsonapi](https://marshmallow-jsonapi.readthedocs.org/en/latest/).

~~~
pip install -r requirements.txt

# Only on Raspberry Pi:
sudo apt-get install python-dev  
pip install rpi.gpio
~~~

If the RPi.GPIO is not installed, the program will use a mockup (which won't switch anything and just logs switching attempts).

### Prepare Frontend

Make sure you have `npm` and `bower` installed.

Install the dependencies:

```bash
cd <project-root>/Client
npm install
```

###  Start the development Server

When starting the server for the first time, we need to create a new database. Run the command with the `--create` switch.

#### Start the backend

~~~bash
cd <project-root>/Flask-Server
source venv/bin/activate
python server.py --file schedule.sqlite
~~~

Options for server.py:

`--create` creates a new database and erases the old if it exists.

`--debug` runs the server in debug mode.

`--file <path-to-file>` is the path to the file where the schedule is stored.

#### run the frontend

```bash
cd <project-root>/Client
gulp
```
