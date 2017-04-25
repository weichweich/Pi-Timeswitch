# Development Installation 

Here you will learn how to install this project on your PC. Because this project is intended for usage with a raspberry pi there will be no real switching of GPIOs (also your PC may not have those).

## Requirements

The following software has to be installed.

- Python 3.x
- pip
- Node Package Manager (npm)

## Prepare Flask-Backend

At first i recommend to create a virtual environment using [Virtualenv](https://virtualenv.pypa.io/en/stable/).

Install Virtualenv:

```
pip install virtualenv
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


Then you need to install the backend dependencies.

```
pip3 install -r requirements.txt
```

## Prepare Frontend


Install the dependencies:

```bash
cd <project-root>/Client
npm install
```

##  Start the development Server

When starting the server for the first time, we need to create a new database. Run the command with the `--create` switch.

### Start the backend

```bash
cd <project-root>/Flask-Server
source venv/bin/activate
python3 server.py --file schedule.sqlite
```

Options for server.py:

`--create` creates a new database and erases the old if it exists.

`--debug` runs the server in debug mode.

`--file <path-to-file>` is the path to the file where the schedule is stored.

### run the frontend

```bash
cd <project-root>/Client
gulp
```
