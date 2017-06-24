"""Airtable client
"""
import requests
import json
import re

API_URL = 'https://api.airtable.com/v0/'


def format_url(base_url, *resources):
    return '/'.join([str(r) for r in resources if r])


class AirtableException(Exception):
    """An exception occurred while polling the server
    """

    def __init__(self, err=None):
        super().__init__(err)
        self.err = err


class ConversionException(Exception):
    """Could not parse JSON response data to dict
    """
    pass


class AirtableBase:
    """Represents an Airtable base

    This class represents an entire Airtable base. The name of the table
    """

    def __init__(self, base_id, api_key):
        self.base_id = base_id
        self.api_key = api_key

        self.url = f"{API_URL}{base_id}"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': 'application/json',
        }

    def retrieve(self, table_name, record_id=None, **params):
        """Retrieve records from the Airtable base.
        """
        url = format_url(self.url, table_name, record_id)

        res = requests.get(url, params)
        if res.status_code not in range(200, 300):
            pass

        try:
            return res.json()
        except ValueError as ve:
            raise ConversionError()

    def create(self):
        pass

    def read(self, id=None):
        pass

    def update(self):
        pass

    def delete(self):
        pass
