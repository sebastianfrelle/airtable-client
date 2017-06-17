"""Tutorial: testing

Playing around with setting up a Python application with tests
"""
from setuptools import setup, find_packages

setup(
    name="airtable_client",
    version="0.1",

    # packages
    packages=find_packages(),

    # requirements
    install_requires=[
        'requests>=2',
    ],

    test_suite="tests",

    # Author info
    author="Sebastian Frelle Koch",
    author_email="sebastian.frelle@gmail.com",
    keywords="airtable client http api",
)
