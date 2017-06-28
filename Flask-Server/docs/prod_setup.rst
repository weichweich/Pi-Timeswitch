
Installation on Raspberry Pi
============================

Currently the project is in an **early state of development**. There are several **bugs** in the GUI and some features are missing.

Requirements
------------

The following software has to be installed.

- Python 3.x
- pip

Install Dependencies
--------------------

At first prepare the raspberry pi:

.. code-block:: bash

    sudo apt install python3 python3-pip python3-dev libssl-dev libffi-dev libpcre3 libpcre3-dev build-essential nginx
    pip3 install virtualenv

Put every thing in place and start nginx
----------------------------------------

There are two options to get the source files of this project.

**First of all**, clone the repository. This way you will get the lates version which may have the newest feature and bug fixes. But you have to consider that the newest version is not as much tested as the release version.

Clone the repository with ``git clone https://github.com/weichweich/Pi-Timeswitch.git``

**The second option** is to download the `release version <https://github.com/weichweich/Pi-Timeswitch/releases/>`_ and unzip it with ``unzip timeswitch-x.y.z.zip``.

After you have downloaded the source files, copy them into there destination.

.. code-block:: bash

    cp timeswitch-x.y.z/frontend /var/www/timeswitch
    cp timeswitch-x.y.z/backend /home/pi/timeswitch
    cp timeswitch-x.y.z/timeswitch.nginx_conf /etc/nginx/sites-available/timeswitch

    sudo chown -R www-data /var/www/timeswitch
    sudo chown -R www-data /home/pi/timeswitch

    sudo ln -s /etc/nginx/sites-available/timeswitch /etc/nginx/sites-enabled/
    sudo service nginx restart

Install backend dependencies
----------------------------

Go to the backend directory. Create a virtual environment and install all requiremets.

.. code-block:: bash

    cd /home/pi/timeswitch
    virtualenv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    pip3 install rpi.gpio uwsgi

Start the backend
-----------------

.. code-block:: bash

    cd /home/pi/timeswitch
    source venv/bin/activate

Initiat the database with:

.. code-block:: bash

    sudo python --create --file timeswitch.sqlite

Whene the database is created, start uwsgi:

.. code-block:: bash

    sudo ./venv/bin/uwsgi --ini timeswitch.ini --pyargv "--file timeswitch.sqlite"

Security
--------

The back- and frontend is not tested for security. It is not recommended to expose the webserver to the internet.

To secure the backend replace the secret key 'secret' (file server.py line 78) with a real secret key and change the username and password (url: <your PI>#/users).

Even if you follow these advice, the backend will not be secure. All userdata, including username and password, will be transmittet in cleartext!
