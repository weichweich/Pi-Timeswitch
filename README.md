# Pi-TimeSwitch
Pi-TimeSwitch is an automated, easy to use timeswitch for the [Raspberry Pi](https://www.raspberrypi.org).

Pi-TimeSwitch provides a web based GUI where one can specify a schedule for every gpio. Start and end time of each intervall can be randomized.

Currently the project is in an **early state of development**. There are several **bugs** in the GUI and some features are missing.

**You are welcome to contribute.**

## How to install Pi-TimeSwitch:

Upgrade pip:

~~~
sudo pip install —upgrade pip
~~~

Install [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

~~~
sudo pip install virtualenv
~~~

Make directory for the repository and go to home folder

~~~
mkdir ~/piSwitch
cd ~
~~~

Clone git repository:

~~~
git clone https://github.com/weichweich/pi-timeswitch.git ./piSwitch
cd ~/piSwitch
~~~

Install [Flask](http://flask.pocoo.org), [Flask-Restful](http://flask-restful.readthedocs.org/en/0.3.4/), [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO)
 
~~~
pip install Flask
pip install Flask-Restful
pip install -U marshmallow --pre # http://marshmallow.readthedocs.org/en/latest/
pip install RPi.GPIO
~~~

Create the SQLite database and start the server:

~~~
python server.py --file schedule.sqlite3 --create
~~~

--create will delete the current SQL database if existing and creates a new one.
