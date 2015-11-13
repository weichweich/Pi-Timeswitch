# Pi-TimeSwitch
Pi-TimeSwitch is an automated, easy to use timeswitch for the [Raspberry Pi](https://www.raspberrypi.org).

Pi-TimeSwitch provides a web based GUI where one can specify a schedule for every gpio. Start and end time of each intervall can be randomized.

The GUI is made using [Emberjs](http://emberjs.com) for a nice interactive website and [Flask](http://flask.pocoo.org) for a simple REST API.

Currently the project is in an **early state of development**. There are several **bugs** in the GUI and some features are missing.

**You are welcome to contribute.**

## How to install Pi-TimeSwitch:

Ensure that pip is installed:

~~~
sudo easy_install pip
~~~

### Virtualenv

At first i recommend to create a virtual environment using [Virtualenv]().

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

### Prepare Flask-Server

Then you need to install [Flask](http://flask.pocoo.org), [Flask-Restful](http://flask-restful.readthedocs.org/en/0.3.4/), [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO), [marshmallow](http://marshmallow.readthedocs.org/en/latest/), [marshmallow-jsonapi](https://marshmallow-jsonapi.readthedocs.org/en/latest/).

~~~
pip install Flask
pip install flask-restful
pip install -U marshmallow --pre
pip install marshmallow-jsonapi
sudo apt-get install rpi.gpio		# Only on Raspberry Pi. 
~~~

If the RPi.GPIO is not installed, the programm will use a mockup (which won't switch anything and just logges switching attempts).

### Prepare Ember-Client

Install [emberjs](http://emberjs.com).

~~~
npm install -g ember-cli
~~~


###  Start the development Server

When starten the server for the fisrt time, we need to create a new database. Run the command with the `--create` switch. 

~~~
cd <project-root>/Flask-Server
source venv/bin/activate
python server.py --file schdule.sqlite

cd <project-root>/Ember-Client/pi-timeswitch
ember server --proxy http://127.0.0.1:5000
~~~

`--create` creates a new database and erases the old if it exists.

`--debug` runns the server in debug mode.

`--file <path-to-file>` is the path to the file where the schedule is stored.
