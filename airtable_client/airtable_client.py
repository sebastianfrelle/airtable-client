"""Airtable client
"""
import requests
import json
import re

API_URL = 'https://api.airtable.com/v0/'


def format_url_params(params):
    url_params = ["{}={}".format(k, v) for k, v in params.items()]
    return '&'.join(url_params)


class AirtableException(Exception):
    """An exception occurred while polling the server
    """

    def __init__(self, err=None):
        super().__init__(err)


class InvalidTableNameException(Exception):
    """An invalid table name was provided.
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

    def _format_url(self, base_id, table_name,
                    identifiers=None, **params):
        if identifiers is None:
            identifiers = []

        # Sanitize and validate table name
        hit = re.search(r'[^/]+', table_name)
        if not hit:
            raise InvalidTableNameException()

        table_name = hit.group(0)

        components = (API_URL, base_id, table_name, *identifiers)
        return '/'.join(components)

    def retrieve(self, table_name, record_id=None, **params):
        """Retrieve records from the Airtable base.
        """

        res = requests.request('GET', url, headers=self.headers)

        return records

    def create(self):
        pass

    def read(self, id=None):
        pass

    def update(self):
        pass

    def delete(self):
        pass
