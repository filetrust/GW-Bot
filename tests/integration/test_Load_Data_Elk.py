import json
from unittest import TestCase

import requests
from osbot_aws.apis.Secrets import Secrets
from pbx_gs_python_utils.utils import Http
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Elastic_Search import Elastic_Search

from gw_bot.helpers.Test_Helper import Test_Helper


class Load_Data_Elk:

    def __init__(self):
        self.oss_server     = 'https://open-security-summit.org'
        self.aws_secret_id  = 'elk-oss-data'
        self.index_id       = 'oss-metadata'
        self._elastic       = None

    def elastic(self):
        if self._elastic is None:
            self._elastic = Elastic_Search(index=self.index_id, aws_secret_id = self.aws_secret_id)
        return self._elastic

    def set_elk_index(self, index_id):
        self.index_id = index_id
        self._elastic = None        # to force reseting the connection
        return self

    def get_data(self,path):
        url = "{0}{1}".format(self.oss_server, path)
        return requests.get(url).json()

    def send_data_to_elk(self, data, create_index=False):
        if create_index:
            self.elastic().delete_index().create_index()
        try:
            records_added = self.elastic().add_bulk(data)
            return { 'status':'ok','data': records_added }
        except Exception as error:
            return {'status': 'error', 'data': '{0}'.format(error) }



class test_Load_Data_Elk(Test_Helper):
    def setUp(self):
        super().setUp()
        self.load_data_elk = Load_Data_Elk()

    def test_data(self):
        data = self.load_data_elk.get_data('/api/index.json')
        assert len(data) > 100

    def test_send_data_to_elk(self):
        data = self.load_data_elk.get_data('/api/index.json')
        self.result = self.load_data_elk.send_data_to_elk(data, create_index=True)

    def test_data_participants(self):
        path = '/participant/api/index.json'
        data = self.load_data_elk.get_data(path)
        self.result = len(data)


    def test_load_local_data(self):
        index_id = 'participants'
        data = requests.get('http://localhost:1313/participant/json/').json()
        self.result = self.load_data_elk.set_elk_index   (index_id)                 \
                                        .send_data_to_elk(data, create_index=True)

        #for item in data:
        #    print(item.get('title'),item.get('word_count'))






