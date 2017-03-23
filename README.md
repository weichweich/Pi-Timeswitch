# Pi-TimeSwitch
Pi-TimeSwitch is an automated, easy to use timeswitch for the [Raspberry Pi](https://www.raspberrypi.org).

Pi-TimeSwitch provides a web based GUI where one can specify a schedule for every gpio. Start and end time of each intervall can be randomized.

Currently the project is in an **early state of development**. There are several **bugs** in the GUI and some features are missing.

## How to install Pi-TimeSwitch:

Ensure that pip is installed:

```
sudo easy_install pip3
```

### Virtualenv

At first i recommend to create a virtual environment using [Virtualenv](https://virtualenv.pypa.io/en/stable/).

Install Virtualenv:

```
pip3 install virtualenv
```

Create a virtual environment:

```
cd <ProjectFolder>/Flask-Server
virtualenv venv
```
Activate it:

```
source venv/bin/activate
```

### Prepare Flask-Backend

Then you need to install the backend dependencies.

```
pip3 install -r requirements.txt

# Only on Raspberry Pi:
sudo apt install python3 python3-pip python3-dev libssl-dev libffi-dev libpcre3 libpcre3-dev build-essential
pip install rpi.gpio uwsgi
```

If the RPi.GPIO is not installed, the program will use a mockup (which won't switch anything and just logs switching attempts).

### Prepare Frontend for development

Make sure you have `npm` installed.

Install the dependencies:

```bash
cd <project-root>/Client
npm install
```

###  Start the development Server

When starting the server for the first time, we need to create a new database. Run the command with the `--create` switch.

#### Start the backend

```bash
cd <project-root>/Flask-Server
source venv/bin/activate
python3 server.py --file schedule.sqlite
```

Options for server.py:

`--create` creates a new database and erases the old if it exists.

`--debug` runs the server in debug mode.

`--file <path-to-file>` is the path to the file where the schedule is stored.

#### run the frontend

```bash
cd <project-root>/Client
gulp
```

## Deployment on Raspberry Pi (raspbian-jessie-lite)

Install dependencies:

```
sudo apt install python3 python3-pip python3-dev libssl-dev libffi-dev libpcre3 libpcre3-dev build-essential nginx
pip install virtualenv
```

Clone the project and create an virtual environment:

```
git clone https://github.com/weichweich/Pi-Timeswitch.git
cd Pi-Timeswitch/Flask-Server
virtualenv venv
pip install -r requirements.txt
pip install uwsgi
python server --create --file typeswitch.sqlite #kill the server after the file was created
```

uwsgi will run as user www-data, so we have to give www-data the ownership of the python sources

```
sudo chown -R www-data .
```

than we have to copy the nginx config, and resart nginx

```
cp ../timeswitch.nginx_conf /etc/nginx/sites-available/timeswitch
sudo ln -s /etc/nginx/sites-available/timeswitch /etc/nginx/sites-enabled/
sudo service nginx restart
```

than start uwsgi

```
sudo ./venv/bin/uwsgi --ini timeswitch.ini --pyargv "--file timeswitch.sqlite"
```