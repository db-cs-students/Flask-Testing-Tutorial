# Flask-Testing-Tutorial

## Overview

In this tutorial, you'll learn how to setup Pytest and write some basic tests for an application. We will explore two types of tests:

- **Functional Tests** - validates the software against the functional requirements/specifications
- **Unit Tests** - validates the smallest testable parts of an application, called units

Additionally, we will explore the idea of Test Driven Development. TDD is the process of writing tests first based on the specifications of the software. These tests will fail initially, and then code is written to ensure that they pass.

## Tutorial

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

def test_find_user(client):
    response = client.get('/user/bob')
    response_json = json.loads(response.data.decode('utf8'))

    assert response.status_code == 200
    assert response_json['lname'] == "Newby"

```

Running pytest should result in a failing test. That is because our app does not have a route for users. Let's create a route to handle this. Open the `__init__.py` in the `my_app` directory. Add a new route like below.

```python
@app.route('/user/<user>')
def get_user(user):
    result = find_user(user)

    if result != None:
        return jsonify(results)

    return "No user found", 404
```

Now you should be able to rerun `pytest` and see a passing test.
