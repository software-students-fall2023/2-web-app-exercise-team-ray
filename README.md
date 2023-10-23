# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

We want to develp a mobile application that connect students with experienced college counselors, providing a platform for high school students to find the ideal college consultant that fits their needs.

## User stories

- As a high school student, I want to see testimonials from past students who used a specific college consulting agency so that I can gauge the success rate and satisfaction of their services.
- As a college counselor/college consulting agency, we want to connect with high school students so that we can help them plan and prepare for his/her personal statement's storyline in their college application.
- As a college student, I want to write reviews for the college consulting agency that helped me when I was in high school.
- As a high school student, I want to find a college counselor so that he/she can help me to navigate the college application process smoothly.
- As a college consulting agency, I want to make our past students' college admission statistics public to people who would potentially be our clients.
- As a consulting agency, I want to know what our competitors offer and the rank of our business in the market in order to adjust the price of our services to a reasonable and attractive level.

## Task boards

sprint #1
https://collisionnyc.atlassian.net/jira/software/projects/SWAS1/boards/3

sprint #2
https://collisionnyc.atlassian.net/jira/software/projects/SWAS2/boards/2

## Intruction to set up the application
## Setup for editing

The following instructions show you how to set up the example app on your own computer in a way that allows you to edit it.

### Build and launch the database

If you have not already done so, start up a MongoDB database:

- run command, `docker run --name mongodb_dockerhub -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret -d mongo:latest`

The back-end code will integrate with this database. However, it may be occasionally useful interact with the database directly from the command line:

- connect to the database server from the command line: `docker exec -ti mongodb_dockerhub mongosh -u admin -p secret`
- show the available databases: `show dbs`
- select the database used by this app: `use example`
- show the documents stored in the `messages` collection: `db.messages.find()` - this will be empty at first, but will later be populated by the app.
- exit the database shell whenever you have had your fill: `exit`

If you have trouble running Docker on your computer, use a database hosted on [MongoDB Atlas](https://www.mongodb.com/atlas) instead. Atlas is a "cloud" MongoDB database service with a free option. Create a database there, and make note of the connection string, username, password, etc.

### Create a `.env` file

A file named `.env` is necessary to run the application. This file contains sensitive environment variables holding credentials such as the database connection string, username, password, etc. This file should be excluded from version control in the [`.gitignore`](.gitignore) file.

An example file named `env.example` is given. Copy this into a file named `.env` and edit the values to match your database. If following the instructions and using Docker to run the database, the values should be:

```
MONGO_DBNAME=example
MONGO_URI="mongodb://admin:secret@localhost:27017/example?authSource=admin&retryWrites=true&w=majority"
```

The other values can be left alone.

### pip

Note that most Python programs require the use of the package manager named `pip` - the default Python "package manager". A package manager is software that takes care of installing the correct version of any modules in the correct place for the current system you are running it on. It comes with most distributions of Python. On many machines, the Python 3-compatible version it is calld `pip3` and on others it is simply `pip`... on some either works. If you are unsure, try both in the commands where you see it mentioned.

### Set up a Python virtual environment

There are multiple ways to set up a Python virtual environment - a specific area of memory and disk space where you can install the dependencies and settings necessary to run a specific app in isolation from other apps on the same computer... here are instructions for using either `pipenv` or `venv`.

### Using pipenv

The ability to make virtual environemnts with [pipenv](https://pypi.org/project/pipenv/) is relatively easy, but it does not come pre-installed with Python. It must be installed.

Install `pipenv` using `pip`:

```
pip3 install pipenv
```

Activate it:

```
pipenv shell
```

Your command line will now be running within a virtual environment.

The file named, `Pipfile` contains a list of dependencies - other Python modules that this app depends upon to run. These will have been automatically installed into the virtual environment by `pipenv` when you ran the command `pipenv shell`.

#### Using venv

If you refuse to use `pipenv` for some reason, you can use the more traditional [venv](https://docs.python.org/3/library/venv.html) instead. The ability to make virtual environments with `venv` comes included with standard Python distributions.

This command creates a new virtual environment with the name `.venv`:

```bash
python3 -m venv .venv
```

To activate the virtual environment named `.venv`...

On Mac:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate.bat
```

The `pip` settings file named, `requirements.txt` contains a list of dependencies - other Python modules that this app depends upon to run.

To install the dependencies into the currently-active virtual environment, use `pip`:

```bash
pip3 install -r requirements.txt
```

### Run the app

- define two environment variables from the command line:
  - on Mac, use the commands: `export FLASK_APP=app.py` and `export FLASK_ENV=development`.
  - on Windows, use `set FLASK_APP=app.py` and `set FLASK_ENV=development`.
- start flask with `flask run` - this will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.
- in some cases, the command `flask` will not be found when attempting `flask run`... you can alternatively launch it with `python3 -m flask run --host=0.0.0.0 --port=5000` (or change to `python -m ...` if the `python3` command is not found on your system).

Note that this will run the app only on your own computer. Other people will not be able to access it. If you want to allow others to access the app running on your local machine, try using the [flask-ngrok](https://pypi.org/project/flask-ngrok/) module.
