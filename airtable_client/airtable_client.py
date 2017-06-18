"""Airtable client
"""
import requests
import json


def format_url_param_str(params):
    url_params = [f"{k}={v}" for k, v in params.items()]
    return '?' + '&'.join(url_params)


class UnknownParamException(Exception):
    """An unknown param was passed to a request.
    """

    pass


class AirtableException(Exception):
    """An exception occurred while polling the server
    """

    def __init__(self, msg=None):
        super().__init__()
        self.msg = msg


class Airtable:
    """Represents an Airtable table
    """

    def __init__(self, base_url, table_name, api_key):
        self.base_url = base_url
        self.table_name = table_name
        self.api_key = api_key

        self.url = base_url + table_name
        self.auth_header = {'Authorization': f'Bearer {api_key}'}

    def _request(self, method, params=None, data=None):
        url = self.url
        if params:
            url += format_url_param_str(params)

        headers = self.auth_header
        if method in ['POST', 'PUT', 'UPDATE']:
            headers['Content-type'] = 'application/json'

        res = requests.request(method, url, headers=headers, data=data)

        parsed_res = res.json()

        if res.status_code not in range(200, 300):
            msg = parsed_res.get('error')
            raise AirtableException(msg)

        return parsed_res

    # CRUD operations
    def get(self, **params):
        """Issue a GET request

        This fetches table records.
        """

        res = self._request('GET', params)
        records = res['records']

        return records

    def post(self, data):
        """Issue a POST request
        """
        pass

    def create(self):
        pass

    def read(self, id=None):
        pass

    def update(self):
        pass

    def delete(self):
        pass
