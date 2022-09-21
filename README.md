# Flask-Testing-Tutorial

## Overview

In this tutorial, you'll learn how to setup Pytest and write some basic tests for an application. We will explore two types of tests:

- **Functional Tests** - validates the software against the functional requirements/specifications
- **Unit Tests** - validates the smallest testable parts of an application, called units

Additionally, we will explore the idea of Test Driven Development. TDD is the process of writing tests first based on the specifications of the software. These tests will fail initially, and then code is written to ensure that they pass.

## Tutorial

In order to follow along with the tutorial, you'll need to clone this respository and have Python 3 installed. The tutorial is written for Flask 2.2.x and Pytest 7.1.x.

### Step 1 - Setup

In the setup process, we will be creating virtual environment for our application, and then we will install the necessary modules. After everything is installed, we will configure the application to run the tests.

First, we will need to setup a virtual environment. Before we do that make sure that you have Python setup on your local machine. Run the following comment in the terminal.

```bash
python --version
```

If python is not found, please ask for help installing it. Now that we have cofirmed that Python is available, let's setup our virtual environment.

```bash
python -m venv venv
source venv/bin/activate
```

This will utilize a python module named `venv` to create a new environment stored in a folder named `venv`. The folder could be named something else, but our .gitignore is set to ignore direcories named `venv`. The second commend sets the source for all of our executables. Rather than running from the `bin` directory on our local machine, it will utilize the new virtual enviroment.

If you have successfully activated the virtual environment, you will see `(venv)` at the beginning of your prompt. In order to deactivate the virtual environment, you can just type `deactivate` to return to you normal system's path.

Secondly, we need to add a configuration file for our app. This will allow us to configure and run our app from within our tests. Create a new file named `setup.py` in the main directory.

```python
from setuptools import setup, find_packages

setup(
    name='my_app',
    version='1.0',
    packages=find_packages(include=['my_app', 'my_app.*'])
)
```

Now let's install some Python modules.

```bash
pip install flask
pip install pytest
pip freeze > requirements.txt
```

This will install our modules in the virtual environment, and the last line saves those into our requirements.txt. Additionally, we will install our `my_app` as a module so it can be called in the tests later.

```bash
pip install -e .
```

This command searches for the setup.py we created, and installs the application in our virtual environment. The `-e` allows us to make changes to the app without having to reinstall it every time.

Now that we have all the packages installed, we need to create the setup for the tests. Create a directory named `tests`. Inside it create a new file named `conftest.py`. Inside that file we'll put the following.

```python
import os
import pytest
from my_app import create_app

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
```

This will setup some basic context for our tests to run. The first fixture is calls the application factory pattern and creates an instace of our application. This does not start a server though, so it can run fairly quick.

The other two fixtures allow us to make calls to our app. This will allow us to do things like make GET or POST requests and look at the responses from the application.

### Step 2 - Writing Tests

The next step will be writing tests in order to confirm our application is working as the specifications intend. Our first test will be a functional test, which will make sure that our application factory is working.

Create a new file in the `tests` directory named `test_factory.py`. All tests should begin with the prefix `test_` followed by a descriptive name of what is being tested. These show up when we run our tests, so they need to provide us with insights as to what the test is doing. In the file we are going to add the following.

```python
from my_app import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    response = client.get('/')
    assert response.data == b'Hello, earth!'
```

We start by importing our application factory since that is what we are primarily testing. Note that this is not always necessary, and the second test would not require this import. The first test is acutally going to run our application factory twice and assert whether it is in testing or not testing configuration. Go check the `my_app/__init__.py` to see what this changes.

The test is just a simple function that we define, and it should be prefixed with `test_` followed by a description of the test. This will also be visible when we run the tests, so think carefully about naming. The `assert` keyword tests whether the condition is true. If it is not it will throw an error and the test will fail. Notice here we test both the possible configurations using the `not` logicial operator.

The second test use the client fixture we setup in the `testconf.py` to make a GET request for the index route. The response data is then checked to ensure it contains certain text. Note that the response data is sent back in byte string format. Here we add a `b"string"` to compare to so that the test will check the correct data type.

That is it for functional tests. We will write another test here in another step, but now let's look at how to run your test.

### Step 3 - Running Tests

Running the test is easy. In the terminal run the following command.

```bash
pytest
```

If everything works correctly, you should see output that confirms that everything works.

Now let's write a test that fails. Create a new file in the tests directory named `test_user.py`. Then let's add the following.

```python
from flask import json

def test_get_user(client):
    response = client.get('/user/bob')
    response_json = json.loads(response.data.decode('utf8'))

    assert response.status_code == 200
    assert response_json['lname'] == "Newby"

```

Running pytest should result in a failing test. That is because our app does not have a route for users. Let's create a route to handle this. Open the `__init__.py` in the `my_app` directory. Add a new route like below.

```python
@app.route('/user/<username>')
def get_user(username):
    result = find_user(username)

    if result != None:
        return jsonify(results)

    return "No user found", 404
```

Now you should be able to rerun `pytest` but you will still see a failing test. Upon examining the output, you may realize that we made a request for `/user/bob` but the list of users includes `Bob`. This should be easy to fix, but through test driven development we were able to catch it quickly. Let's only the `my_app/__init__.py` and modify our `find_user` function to make everything lower case. Find the line

```python
if user == line['fname']:
```

and change it to

```python
if user.lower() == line['fname'].lower():
```

Great, let's go back to our test and add a few more tests to deal with other cases that might occur. When you are writing tests, it is important to think about edge cases. These are the situations where the users is at the 'edge' of possible inputs. For example, if you are dealing with a range of numbers 1-10 as possible outputs. Our test cases should include a number in the middle, the begining of the range (i.e. 1), the end of the range (i.e. 10), and numbers outside the range (i.e. 100). By writing tests for all these possiblilites we are more likely to catch errors in our application's logic. In the case of the app in the tutorial, uppercase and lowercase inputs would be an edge. Let's rewrite our first test to make it a bit more specific. Change the name of the test and add the assert statements at the bottom like below.

```python
def test_get_user_bob(client):
    response = client.get('user/Bob')
    response_json = json.loads(response.data.decode('utf8'))

    assert response.status_code == 200
    assert response_json['lname'] == "Newby"
    assert not response_json['lname'] == "Hopper"
```

Now we can duplicate this test with another user in our list.

```python
def test_get_user_jim(client):
    response = client.get('user/jim')
    response_json = json.loads(response.data.decode('utf8'))

    assert response.status_code == 200
    assert response_json['lname'] == "Hopper"
    assert not response_json['lname'] == "Newby"
```

We can also test for a user not in the list.

```python
def test_get_user_not_found(client):
    response = client.get('user/not%20found')

    assert response.status_code == 404
    assert response.data == b"No user found"
```

Also since we might be repeating the conversion to json in most of our tests, we can extract that into a helper function. At the top of our test, add a new function.

```python
def response_json(response):
    return json.loads(response.data.decode('utf8'))
```

Now we can refactor our previous tests to use this new function. For example, the first test would now look like this:

```python
def test_get_user_bob(client):
    response = client.get('user/Bob')

    assert response.status_code == 200
    assert response_json(response)['lname'] == "Newby"
```

If you use it more than once within a test, it may be worth setting up a variable to store the new json data. For example, the second test would now look like this:

```python
def test_get_user_jim(client):
    response = client.get('user/jim')
    json = response_json(response)

    assert response.status_code == 200
    assert json['lname'] == "Hopper"
    assert not json['lname'] == "Newby"
```

**Your Turn:** Try creating another test following this pattern that might test an edge case.

### Step 4 - Writing Unit Tests

Now that we looked at several examples of functional tests, let's look at an example of an unit test. We really only have one unit to test in our app right now and that is the `find_user` function. Here we can test this function sepearately from the functional application of it in the user route.

Create a new file in your `tests` directory named `test_find_user.py`, and then lets write a simple test.

```python
from my_app import find_user


def test_find_user():
    assert find_user('bob')['lname'] == 'Newby'
    assert find_user('JIM')['lname'] == 'Hopper'
    assert find_user('DuStIn')['lname'] == 'Henderson'
    assert find_user('mIKE')['lname'] == 'Wheeler'
    assert find_user('Bailey') == None
```

Here we just have a single test, but multiple assertions are made to test various capitalization and users not in the list. These tests can be helpful when a bug is occuring in the functional tests. You can quickly eliminate a unit as being the culprit and move on to narrowing down the location of the bug.

**Important** - Go ahead and commit your code up to this point with the commit message `Complete tutorial`. Push your code to the remote repository. This will indicate that you are finished and will be the part of this assignment I go in to grade.

### Step 5 - Your Turn

Start a new branch named `my_turn`. Since the tutorial has been completed on the main brach, and you have committed the compled code there, you now have a space to make mistakes and experiment. You will be adding a new test and then implementing a new feature to pass that test.

The feature you will be implementing is to get a user's birthday. Start by creating a new file in the `tests` directory named `test_get_birthday.py`. Write a test that will request a resource that includes the user's birthday. Be sure you think carefully about the route and what some of the possible return data would look like (i.e. json or raw data).

Additionally, you will write a unit test for the search function that will find the user's birthday. Create a new file in `tests` named `test_find_birthday`. You will import this from your app, and create a few assersions to test various edge cases.

**Important** Commit the new test with the commit message `Write test first`. This will prove to me that you wrote the test before trying to implement the feature.

Next jump into the app and modify the user data to include a new key/value pair that includes a birthday - bonus if you can find the actual birthdays for the characters. Then implement a new route to return the data and a new function for finding the data in the list.

Run your tests and fix any errors or issues until the tests all pass.

**Important** Commit the work code with the commit message `Implement feature with passing tests`. Then be sure you push your branch to your remote repository.

## Conclusion

You now have written several different types of tests that ensure that the code will not break as we add features and make changes to the data. While tests do not prevent us from making mistakes they do help us catch them earlier and help us idenify where the error has occured. Pytest has may more cool features and plugins that can enhance the output of the tests. Be sure to explore the documentation of pytest at https://docs.pytest.org/ and you can see plugins available at https://docs.pytest.org/en/7.0.x/reference/plugin_list.html.

Go to Canvas and provide a link to your remote repository. Then answer the prompts to finish up this tutorial.
