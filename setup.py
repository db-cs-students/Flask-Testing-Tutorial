from setuptools import setup, find_packages

setup(
    name='my_app',
    version='1.0',
    packages=find_packages(include=['my_app', 'my_app.*'])
)
