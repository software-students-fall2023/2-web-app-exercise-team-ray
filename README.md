# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

As the “Yelp of education consulting,” CollegePro is a mobile application that connect students with experienced college counselors, providing a platform for high school students to find the ideal college consultant that fits their needs.

## User stories

- As a high school student, I want to see testimonials from past students who used a specific college consulting agency so that I can gauge the success rate and satisfaction of their services.
- As a college counselor/college consulting agency, we want to connect with high school students so that we can help them plan and prepare for his/her personal statement's storyline in their college application.
- As a college student, I want to write reviews for the college consulting agency that helped me when I was in high school.
- As a high school student, I want to find a college counselor so that he/she can help me to navigate the college application process smoothly.
- As a college consulting agency, I want to make our past students' college admission statistics public to people who would potentially be our clients.
- As a consulting agency, I want to know what our competitors offer and the rank of our business in the market in order to adjust the price of our services to a reasonable and attractive level.

## Task boards

sprint #1
https://github.com/orgs/software-students-fall2023/projects/67/views/2

sprint #2
https://github.com/orgs/software-students-fall2023/projects/66/views/2

## Intruction to set up the application
## Setup for editing

The following instructions show you how to set up the example app on your own computer in a way that allows you to edit it.

### Build and launch the database

First, start up a MongoDB database:
- run command, `docker run --name mongodb_dockerhub -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret -d mongo:latest`
The connect to the database server from the command line: `docker exec -ti mongodb_dockerhub mongosh -u admin -p secret`
Hence, select the database used by this app: `use institution_database`.


### Create a `.env` file
A file named `.env` is necessary to run the application. This file contains sensitive environment variables holding credentials such as the database connection string, username, password, etc. This file should be excluded from version control in the [`.gitignore`](.gitignore) file.
The values should be:
```
MONGO_DBNAME=institution_database
MONGO_URI="mongodb://admin:secret@localhost:27017/example?authSource=admin&retryWrites=true&w=majority"
```


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
```
pip3 install -r requirements.txt
```

### Run the app
- define two environment variables from the command line:
  - on Mac, use the commands: `export FLASK_APP=app.py` and `export FLASK_ENV=development`.
  - on Windows, use `set FLASK_APP=app.py` and `set FLASK_ENV=development`.
- start flask with `flask run` - this will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.
