Development Installation
========================

Here you will learn how to install this project on your PC. Because this project is intended for usage with a raspberry pi there will be no real switching of GPIOs (also your PC may not have those).

Requirements
------------

The following software has to be installed.

- Python 3.x
- pip
- Node Package Manager (npm)

Prepare Flask-Backend
---------------------

At first i recommend to create a virtual environment using `Virtualenv <https://virtualenv.pypa.io/en/stable/>`_.

Install Virtualenv:

.. code-block:: bash

    pip install virtualenv


Create a virtual environment:

.. code-block:: bash

    cd <ProjectFolder>/Flask-Server
    virtualenv venv

Activate it:

.. code-block:: bash

    source venv/bin/activate


Then you need to install the backend dependencies.

.. code-block:: bash

    pip3 install -r requirements.txt


Befor the backend can now be started, you need to initialize the database. This is done with the following command, which will exit after its done.

.. code-block:: bash

    python3 server.py --create --file schedule.sqlite

To run the backend, just leaveout the ``--create`` option. This command will run until its killed.

.. code-block:: bash

    python3 server.py --file schedule.sqlite

Prepare Frontent
----------------

Install the dependencies:

.. code-block:: bash

    cd <project-root>/Client
    npm install


Start the development Server
----------------------------

To run the website you need to serve the frontend and the backend. The frontend are just static files which will be served by gulp. All request for the url ``/api`` which are send to the frontend server are redirected to the backend server. Therefor both server has to run simultaneously.

Start the backend
+++++++++++++++++

.. code-block:: bash

    cd <project-root>/Flask-Server
    source venv/bin/activate
    python3 server.py --file schedule.sqlite

Options for server.py:

 ``--create`` creates a new database and erases the old if it exists.

 ``--debug`` runs the server in debug mode.

 ``--file <path-to-file>`` is the path to the file where the schedule is stored.

run the frontend
++++++++++++++++

.. code-block:: bash

    cd <project-root>/Client
    gulp
