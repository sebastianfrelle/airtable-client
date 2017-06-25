"""Unit testing the Airtable client

The test suite is independent of specific Airtable tables and bases, so you'll
have to provide your own data. It is strongly recommended to create an Airtable 
table to run the tests against. The table should have a few, filled-in records 
and an assortment of field types to ensure that any tests that are set up 
dynamically will run without errors.

There is a limit to how precise the tests can be without access to a common, 
open Airtable instance-- obviously, I can't provide my personal Airtable API 
key.
"""

import logging
import random
import string
import unittest

from .constants import API_KEY, BASE_ID, TABLE_NAME, TEST_RECORD
from .context import airtable_client as client

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

        res = self.test_base.retrieve(table_name=TABLE_NAME)
        records = res['records']

        # Get a random record to test with
        test_record = records[random.randrange(len(records))]

        # Find a field in test_record that takes type 'str' to test against
        str_fields = (k for k in test_record['fields'].keys()
                      if isinstance(test_record['fields'][k], str))
        target = next(str_fields, None)
        self.assertIsNotNone(
            target,
            msg="Test table should include a field of type 'str' for this test")
        
        print(f"\nTesting with field {target}")

        # Generate a random string
        test_string = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=20))

        # Update entry in fields
        test_patch = {
            'fields': {target: test_string},
        }

        # Perform update request
        res = self.test_base.partial_update(
            table_name=TABLE_NAME, record_id=test_record['id'], data=test_patch)

        # Check to see if field was properly updated
        self.assertIsNotNone(res)
        self.assertIn(target, res['fields'])
        self.assertEqual(test_record['id'], res['id'])
        self.assertEqual(test_string, res['fields'][target])
