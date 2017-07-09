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

    def __init__(self, code=None, msg=None):
        super().__init__()
        self.code = code
        self.msg = msg


class AirtableBase:
    """Represents an Airtable base

    The name of the table to operate
    """

    def __init__(self, base_id, api_key):
        self.base_id = base_id
        self.api_key = api_key

        self.url = API_URL + base_id
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': 'application/json',
        }

    def _request(self, url, params=None, json=None):
        res = requests.request(method, url, params,
                               headers=self.headers, json=json)

        if res.status_code not in range(200, 300):
            try:
                res.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise AirtableException(code=res.status_code, msg=e.message)

            return AirtableException(msg="Unknown error occurred")

        return res.json()

    def create(self, table_name, data):
        """Create a new record in the Airtable table with name table_name
        """
        url = format_url(self.url, table_name)
        return self._request(url, 'POST', json=data)

    def read(self, table_name, record_id=None, **params):
        """Retrieve records from the Airtable base
        """
        url = format_url(self.url, table_name, record_id)
        return self._request(url, 'GET', params=params)

    def update(self, table_name, record_id, data):
        """Update an entire Airtable record

        Calling this method empties any field that isn't included in the data 
        being sent. Make sure to include any field that you want to keep.
        """
        url = format_url(self.url, table_name, record_id)
        return self._request(url, 'PUT', json=data)

    def partial_update(self, table_name, record_id, data):
        """Update a record in the Airtable table with name table_name
        """

        url = format_url(self.url, table_name, record_id)
        return self._request(url, 'PATCH', json=data)

    def delete(self, table_name, record_id):
        """Delete a record in the Airtable table with name table_name
        """
        url = format_url(self.url, table_name, record_id)
        return self._request(url, 'DELETE')
