"""Airtable client
"""
import requests
import json

API_URL = 'https://api.airtable.com/v0/'


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

    def __init__(self, err=None):
        super().__init__(err)


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

    def _request(self, method, url, data=None):
        return requests.request(method, url, headers=self.headers, data=data)

    def retrieve(self, table_name, record_id=None, **params):
        """Retrieve records from the Airtable base.
        """

        url = self.url + '/' + table_name
        if record_id:
            url += '/' + record_id
        if params:
            url += format_url_param_str(params)

        res = self._request(method='GET', url=url)

        # Error checking here
        if res.status_code not in range(200, 300):
            err = {
                'msg': res.json().get('error'),
                'status_code': res.status_code,
            }
            raise AirtableException(err)

        res_data = res.json()

        return res_data

    def create(self):
        pass

    def read(self, id=None):
        pass

    def update(self):
        pass

    def delete(self):
        pass
