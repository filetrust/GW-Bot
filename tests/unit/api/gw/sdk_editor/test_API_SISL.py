import json
from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from gw_bot.api.gw.skd_editor.API_SISL import API_SISL


class test_API_SISL(TestCase):

    def setUp(self):
        self.sisl = API_SISL()
        self.result = None
        self.path_sisl_zip_file = '/tmp/tmp-input/doc-1.docx.zip'
        self.path_sisl_files    = '/tmp/tmp-input/bbbb.docx'
        self.test_sisl_file     = '/tmp/tmp-input/bbbb.docx/Id_192233350_stream_5.sisl'

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
        json_data["__struct_620: VALUEARRAY"]['__data'] = 'AAAA [Changed from Test] BBB'

        self.sisl.convert_json_to_sisl_file(json_data, target_file)
        self.test_zip_sisl_files()

    def test_unzip_sisl_file(self):
        target_folder = '/tmp/tmp-input/aaaa'
        self.result = self.sisl.unzip_sisl_file(self.path_sisl_zip_file, target_folder)

    def test_zip_sisl_files(self):
        target_folder = '/tmp/tmp-input/aaaa.docx'
        self.result = self.sisl.unzip_sisl_file(self.path_sisl_zip_file, target_folder)
        sisl_files  = self.sisl.zip_sisl_files(target_folder)
        Dev.pprint(sisl_files)

    def test_edit_value_array(self):
        target_file   = '/tmp/tmp-input/doc-1.docx.zip'
        target_folder = '/tmp/tmp-input/bb_123.docx'
        self.sisl.unzip_sisl_file(target_file, target_folder)
        #self.sisl.zip_sisl_files(target_folder)
        self.sisl.edit_value_array(target_folder, "5", "620", "Another value! 123")
        self.result = self.sisl.zip_sisl_files(target_folder)




