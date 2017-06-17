"""Unit testing

** You need ./constants.py with base_url, table_name and api_key 
pointing to the Airtable table you want to test against.**
"""
import unittest
from .context import airtable_client

# Needs constants to run
from .constants import BASE_URL, TABLE_NAME, API_KEY


class TestAirtableClient(unittest.TestCase):
    """Test the Airtable client
    """
