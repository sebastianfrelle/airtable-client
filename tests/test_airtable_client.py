"""Unit testing

** You need ./constants.py with base_url, table_name and api_key
pointing to the Airtable table you want to test against.**

There is a limit to how precise the tests can be without access to
a common, open Airtable instance-- obviously, I can't provide my
personal Airtable API key. For better coverage, I suggest writing
supplementary testing (sorry).
"""
import unittest
from .context import airtable_client as client

# Needs constants to run
from .constants import BASE_URL, TABLE_NAME, API_KEY


class TestAirtableClient(unittest.TestCase):
    """Test the Airtable client
    """

    def setUp(self):
        self.table = client.Airtable(BASE_URL, TABLE_NAME, API_KEY)

    def test_init_table(self):
        """Test initializing the client
        """
        self.assertIsNotNone(self.table)
        self.assertEqual(BASE_URL + TABLE_NAME, self.table.url)

    def test_read_one_record(self):
        """Read first record in table

        Serves to verify connection
        """
        recs = self.table.get(max_records=1)

        self.assertIsNotNone(recs)
        self.assertTrue(isinstance(recs, list))
        self.assertFalse(len(recs) > 1)  # Could be of length 0 or 1

    def test_read_records(self):
        """Read all records in the table
        """
        recs = self.table.get()

        self.assertIsNotNone(recs)
        self.assertTrue(isinstance(recs, list))
