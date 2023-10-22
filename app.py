from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import load_dotenv
import os
import pymongo
import datetime
from bson.objectid import ObjectId
import sys
import os
import subprocess

# instantiate the app
app = Flask(__name__)

load_dotenv()  # take environment variables from .env.

# turn on debugging if in development mode
if os.getenv('FLASK_ENV', 'development') == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode
# connect to the database

cxn = pymongo.MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000)
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    db = cxn[os.getenv('MONGO_DBNAME')] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(' *', "Failed to connect to MongoDB at", os.getenv('MONGO_URI'))
    print('Database connection error:', e) # debug


@app.route('/')
def home():
    """
    Route for the home page
    """
    return render_template('index.html')

@app.route('/student')
def student_portal():
    return render_template('student.html')

@app.route('/institution')
def home_inst():
    """
    Route for the institution home page
    """
    return render_template('home_inst.html') # render the hone template

@app.route('/institution/create', methods=['POST'])
def create_institution():
    """
    Route for POST requests to the create page.
    Accepts the form submission data for a new document and saves the document to the database.
    """
    name_inst = request.form['institutionName']
    year_inst = request.form['foundedYear']
    base_inst = request.form['baseLocation']
    desc_inst = request.form['description']

    # create a new document with the data the user entered
    doc = {
        "name": name_inst,
        "year": year_inst, 
        "base": base_inst,
        "desc": desc_inst,
        "reviews": {},
    }
    db.messages.insert_one(doc) # insert a new document

    return redirect(url_for('home_inst'))


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    if request.method == 'POST':
        review_content = request.form.get('review')
        institution_id = request.form.get('institution_id')  # You must identify the institution somehow
        review = {
            "content": review_content,
            "institution_id": institution_id,
            "created_at": datetime.datetime.utcnow()
        }
        db.reviews.insert_one(review)
        return redirect(url_for('student_portal'))
    return render_template('write_review.html')
    

@app.route('/institution/list')
def list():
    """
    Route for the institution list page
    """
    docs = db.messages.find({}).sort("name", -1) # sort in descending order of created_at timestamp
    return render_template('list.html', docs=docs) # render the hone template


@app.route('/institution/search_result', methods=['POST'])
def search():
    """
    Route for the institution list page
    """
    name_inst = request.form['name_inst']
    base_inst = request.form['base_inst']
    kwrd_inst = request.form['kwrd_inst']

    docs = db.messages.find({"name" :{"$regex" : name_inst, '$options' : 'i'}, "base":{"$regex" : base_inst, '$options' : 'i'}, "desc":{"$regex" : kwrd_inst, '$options' : 'i'} }).sort("name", -1)
    return render_template('list.html', docs=docs) # render the hone template


# @app.route('/list_institutions')
# def list_institutions():
#     institutions = db.institutions.find()
#     return render_template('list_institutions.html', institutions=institutions)


@app.route('/add_institution', methods=['GET', 'POST'])
def add_institution():
    if request.method == 'POST':
        institution_data = {
            "name": request.form.get('name'),
            "description": request.form.get('description'),
            "created_at": datetime.datetime.utcnow()
        }
        db.institutions.insert_one(institution_data)
        return redirect(url_for('institution_portal'))
    return render_template('add_institution.html')

@app.route('/edit/<inst_id>', methods=['POST'])
def edit_inst(inst_id):
    """
    Route for POST requests to the edit page.
    Accepts the form submission data for the specified document and updates the document in the database.
    """

    new_name = request.form['institutionName']
    new_year = request.form['foundedYear']
    new_base = request.form['baseLocation']
    new_desc = request.form['description']

    db.messages.update_one(
        {"_id": ObjectId(inst_id)}, # match criteria
        { "$set": {'name' : new_name, 'year' : new_year, 'base' : new_base, 'desc' : new_desc} }
    )

    return redirect(url_for('list'))

@app.route('/institution/delete/<inst_id>')
def delete_inst(inst_id):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the home page.
    """
    db.messages.delete_one({"_id": ObjectId(inst_id)})
    return redirect(url_for('list'))

@app.route('/read')
def read():
    """
    Route for GET requests to the read page.
    Displays some information for the user with links to other pages.
    """
    docs = db.exampleapp.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    return render_template('read.html', docs=docs) # render the read template

@app.route('/create')
def create():
    """
    Route for GET requests to the create page.
    Displays a form users can fill out to create a new document.
    """
    return render_template('create.html') # render the create template


@app.route('/create', methods=['POST'])
def create_post():
    """
    Route for POST requests to the create page.
    Accepts the form submission data for a new document and saves the document to the database.
    """
    name = request.form['fname']
    message = request.form['fmessage']

    # create a new document with the data the user entered
    doc = {
        "name": name,
        "message": message, 
        "created_at": datetime.datetime.utcnow()
    }
    db.exampleapp.insert_one(doc) # insert a new document
    return redirect(url_for('read')) # tell the browser to make a request for the /read route

@app.route('/edit/<inst_id>')
def edit(inst_id):
    """
    Route for GET requests to the list of institution page.
    Displays a list of existing consulting
    """
    doc = db.messages.find_one({"_id": ObjectId(inst_id)})
    return render_template('edit_inst.html', doc=doc) # render the edit template


# @app.route('/edit/<mongoid>')
# def edit(mongoid):
#     """
#     Route for GET requests to the edit page.
#     Displays a form users can fill out to edit an existing record.
#     """
#     doc = db.exampleapp.find_one({"_id": ObjectId(mongoid)})
#     return render_template('edit.html', mongoid=mongoid, doc=doc) # render the edit template


@app.route('/edit/<mongoid>', methods=['POST'])
def edit_post(mongoid):
    """
    Route for POST requests to the edit page.
    Accepts the form submission data for the specified document and updates the document in the database.
    """
    name = request.form['fname']
    message = request.form['fmessage']

    doc = {
        # "_id": ObjectId(mongoid), 
        "name": name, 
        "message": message, 
        "created_at": datetime.datetime.utcnow()
    }

    db.exampleapp.update_one(
        {"_id": ObjectId(mongoid)}, # match criteria
        { 
            "$set": doc }
    )
    return redirect(url_for('read')) # tell the browser to make a request for the /read route


@app.route('/delete/<mongoid>')
def delete(mongoid):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the read page.
    """
    db.exampleapp.delete_one({"_id": ObjectId(mongoid)})
    return redirect(url_for('read')) # tell the web browser to make a request for the /read route.

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    GitHub can be configured such that each time a push is made to a repository, GitHub will make a request to a particular web URL... this is called a webhook.
    This function is set up such that if the /webhook route is requested, Python will execute a git pull command from the command line to update this app's codebase.
    You will need to configure your own repository to have a webhook that requests this route in GitHub's settings.
    Note that this webhook does do any verification that the request is coming from GitHub... this should be added in a production environment.
    """
    # run a git pull command
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    pull_output = process.communicate()[0]
    # pull_output = str(pull_output).strip() # remove whitespace
    process = subprocess.Popen(["chmod", "a+x", "flask.cgi"], stdout=subprocess.PIPE)
    chmod_output = process.communicate()[0]
    # send a success response
    response = make_response('output: {}'.format(pull_output), 200)
    response.mimetype = "text/plain"
    return response

@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e) # render the edit template


if __name__ == "__main__":
    PORT = os.getenv('PORT', 5000) # use the PORT environment variable, or default to 5000

    #import logging
    #logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(port=PORT)