import json
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files

from gw_bot.api.gw.skd_editor.API_SISL import API_SISL


class test_API_SISL(TestCase):

    def setUp(self):
        self.sisl = API_SISL()
        self.result = None
        self.test_sisl_file = '/tmp/tmp-input/bbbb.docx/Id_192233350_stream_5.sisl'

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_convert_sisl_file_to_json(self):
        json_data = self.sisl.convert_sisl_file_to_json(self.test_sisl_file)
        Dev.pprint(json_data["__struct_620: VALUEARRAY"]['__data'])
        print(json.dumps(json_data,indent=2))

    def test_convert_json_to_sisl(self):
        json_data = self.sisl.convert_sisl_file_to_json(self.test_sisl_file)
        sisl_data = self.sisl.convert_json_to_sisl(json_data)

    def test_convert_json_to_sisl_file(self):
        target_file = self.test_sisl_file
        json_data = self.sisl.convert_sisl_file_to_json(self.test_sisl_file)
        json_data["__struct_620: VALUEARRAY"]['__data'] = 'Changed from Test'
        sisl_data = self.sisl.convert_json_to_sisl_file(json_data, target_file)
        Dev.print(Files.contents(sisl_data))

