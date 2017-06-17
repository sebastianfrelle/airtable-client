"""Airtable client
"""
import requests


class UnknownParamException(Exception):
    """An unknown param was passed to a request.
    """
    pass


class AirtableException(Exception):
    """An exception occurred while polling the server
    """
    def __init__(self, msg):
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

    def _request(self, method, params=None, body=None):
        url = self.url
        if params:
            url += self._format_param_str(params)

        # unfinished

    def _format_param_str(self, params):
        url_params = [f"{k}={v}" for k, v in params.items()]
        return '?' + '&'.join(url_params)

    # get_params = [
    #     'fields', 'maxRecords', 'filterByFormula',
    #     'pageSize', 'sort', 'view',
    # ]

    def get(self, **params):
        """Issue a GET request

        This fetches table records.
        """
        res = self._request('GET', params)

        if res.status_code not in range(200, 300):
            raise Exception()
