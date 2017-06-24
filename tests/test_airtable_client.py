"""Unit testing

** You need ./constants.py with base_url, table_name and api_key
pointing to the Airtable table you want to test against.**

There is a limit to how precise the tests can be without access to
a common, open Airtable instance-- obviously, I can't provide my
personal Airtable API key. For better coverage, I suggest writing
supplementary testing (sorry).
"""

import logging
import unittest

from .context import airtable_client as client
from .constants import BASE_ID, TABLE_NAME, API_KEY, TEST_RECORD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestAirtableClient(unittest.TestCase):
    """Test the Airtable client
    """

    def setUp(self):
        self.test_base = client.AirtableBase(BASE_ID, API_KEY)

    # Tests
    def test_init_table(self):
        """Test initializing the client
        """

        self.assertIsNotNone(self.test_base)

    def test_format_url(self):
        """Test URL formatter
        """

        base_url = 'http://www.foo.com'
        url = client.format_url(base_url, 'foo', None, 'bar')

        self.assertEqual(f"{base_url}/foo/bar", url)

    def test_read_one_record(self):
        """Read first record in table

        Also serves to verify connection.
        """

        res = self.test_base.retrieve(table_name=TABLE_NAME, limit=1)

        self.assertIsNotNone(res)
        self.assertIsInstance(res, dict)
        self.assertIn('records', res.keys())

        records = res['records']
        self.assertIsInstance(records, list)
        self.assertTrue(len(records) in (0, 1))

    def test_read_all_records(self):
        """Read all records in the table
        """

        res = self.test_base.retrieve(table_name=TABLE_NAME)

        self.assertIsNotNone(res)
        self.assertIsInstance(res, dict)
        self.assertIn('records', res.keys())

        records = res['records']
        self.assertIsInstance(records, list)

    def test_create_a_record(self):
        """Create a new record in a table
        """

        res = self.test_base.create(table_name=TABLE_NAME, data=TEST_RECORD)

        self.assertIsNotNone(res)
        self.assertIsInstance(res, dict)
        self.assertIsNotNone(res.get('id'))

        # Assert equal values for keys that exist in both test data and created
        # input
        for k in TEST_RECORD['fields'].keys():
            self.assertEqual(TEST_RECORD['fields'][k], res['fields'][k])

    def test_partially_update_a_record(self):
        """Test partially update a record
        """

        pass
