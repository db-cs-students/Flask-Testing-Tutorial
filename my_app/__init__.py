import os
from flask import Flask, jsonify

users = [
    {"fname": "Will", "lname": "Byers"},
    {"fname": "Bob", "lname": "Newby"},
    {"fname": "Mike", "lname": "Wheeler"},
    {"fname": "Dustin", "lname": "Henderson"},
    {"fname": "Jim", "lname": "Hopper"},
]


def find_user(user):
    for line in users:
        if user.lower() == line['fname'].lower():
            return line
    return None


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, earth!'

    @app.route('/user/<username>')
    def get_user(username):
        result = find_user(username)

        if result != None:
            return jsonify(result)

        return "No user found", 404

    return app
