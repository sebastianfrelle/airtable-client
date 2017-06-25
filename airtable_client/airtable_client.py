"""Airtable client
"""
import requests
import json
import re

API_URL = 'https://api.airtable.com/v0/'


def format_url(*resources):
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

        self.url = API_URL + base_id
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': 'application/json',
        }

    def retrieve(self, table_name, record_id=None, **params):
        """Retrieve records from the Airtable base
        """
        url = format_url(self.url, table_name, record_id)

        res = requests.get(url, params, headers=self.headers)
        if res.status_code not in range(200, 300):
            raise AirtableException({'status_code': res.status_code})

        try:
            return res.json()
        except ValueError as ve:
            raise ConversionError()

    def create(self, table_name, data):
        """Create a new record in the Airtable table with name table_name
        """

        url = format_url(self.url, table_name)

        res = requests.post(url, json=data, headers=self.headers)
        if res.status_code not in range(200, 300):
            raise AirtableException({'status_code': res.status_code})

        try:
            return res.json()
        except ValueError as ve:
            raise ConversionException()

    def partial_update(self, table_name, record_id, data):
        """Update a record in the Airtable table with name table_name
        """

        url = format_url(self.url, table_name, record_id)

        res = requests.patch(url, json=data, headers=self.headers)
        if res.status_code not in range(200, 300):
            raise AirtableException({'status_code': res.status_code})

        try:
            return res.json()
        except ValueError as ve:
            raise ConversionException()

    def update(self, table_name, data):
        """Update an entire Airtable record
        """

        pass

    def delete(self, table_name, record_id):
        """Delete a record in the Airtable table with name table_name
        """

        url = format_url(self.url, table_name, record_id)

        res = requests.delete(url, headers=self.headers)
        if res.status_code not in range(200, 300):
            raise AirtableException({'status_code': res.status_code})

        data = res.json()
        if not data['deleted']:
            raise AirtableException(data)

        try:
            return data
        except ValueError as ve:
            raise ConversionException()
