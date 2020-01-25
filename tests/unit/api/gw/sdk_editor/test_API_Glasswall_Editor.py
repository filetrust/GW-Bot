import json
import os
import sys
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Json import Json
from pbx_gs_python_utils.utils.Process import Process
from pbx_gs_python_utils.utils.Unzip_File import Unzip_File
from pbx_gs_python_utils.utils.Zip_Folder import Zip_Folder

from gw_bot.api.gw.sdk_scanner.API_Glasswall_Docker import API_Docker_Glasswall
from gw_bot.api.gw.skd_editor.API_Glasswall_Editor import API_Glasswall_Editor
from gw_bot.api.gw.skd_editor.API_SISL import API_SISL


class test_API_Glasswall_Editor(TestCase):
    def setUp(self) -> None:
        self.glasswall = API_Glasswall_Editor()
        self.result    = None

    def tearDown(self) -> None:
        if self.result is not None:
            Dev.pprint(self.result)

    def test_ctor(self):
        assert self.glasswall.docker_image == 'glasswallsolutions/evaluationsdk:2'

    def test_glasswall_cli(self):
        #assert self.glasswall.docker_cli(['-v']) == '1.42.33256\nSUCCESS\n'
        self.result =self.glasswall.glasswall_cli(['ls','config'])

    def test_glasswall_scan(self):
        self.result = self.glasswall.glasswall_scan()

    def test_docker_run_bash_command(self):
        assert 'home'                      in self.glasswall.docker_run_bash_command(['ls','/'])
        assert 'glasswallCLI'              in self.glasswall.docker_run_bash_command(['ls'])
        assert 'executable file not found' in self.glasswall.docker_run_bash_command('aaaa')

    def test_scan_file(self):
        file_to_scan = '/tmp/doc-2.docx'
        new_file     = '/tmp/doc-2-NEW.docx'
        self.result = self.glasswall.scan_file(file_to_scan,new_file)

    def test_file_to_sisl(self):
        file_to_scan  = '/tmp/doc-2.docx'
        zip_file = self.glasswall.file_to_sisl(file_to_scan)
        #self.result = zip_file
        self.result = zip_file

    def test_sisl_to_file(self):
        test_folder       = '/tmp/sisl-import-test'
        target_file       = 'doc-2.docx'
        file_to_scan      = f'{test_folder}/{target_file}'                              # Original file to edit
        new_file          = f'{test_folder}/NEW-{target_file}'                          # New file to create
        sisl_stream_id    = '5'                                                         # sisl file that has the content
        sisl_struct_id    = '977'                                                       # location in sisl_stream_id file
        new_text          = 'This IS a NEW content !!!'                                 # new text to go on sisl_struct_id

        glasswall_editor = API_Glasswall_Editor()                                       # API to invoke GW Editor running locally in Docker
        sisl             = API_SISL()                                                   # API to access and manipulate SISL

        sisl_file        = glasswall_editor.file_to_sisl(file_to_scan)                  # GW Engine in Docker to create zip with SISL files (export)
        sisl_folder      = sisl.unzip_sisl_file(sisl_file)                              # extract SISL zip files into temp folder

        sisl.edit_value_array(sisl_folder, sisl_stream_id, sisl_struct_id, new_text)    # to the text replace

        new_sisl_file    = sisl.zip_sisl_files(sisl_folder)                             # zip the SISL files

        glasswall_editor.sisl_to_file(new_sisl_file,new_file)                           # GW Engine in Docker to create new file (import)




    # def test_watermark_file(self):
    #     file_to_scan = '/tmp/gcon-sessions.pdf'
    #     new_file     = '/tmp/gcon-sessions-with-WATERMARK.pdf'
    #     watermark    = 'Twitter Demo'
    #     self.result = self.glasswall.watermark_file(file_to_scan, new_file,watermark)


# class test_Unzip_Bug(TestCase):
#
#     def setUp(self) -> None:
#         self.result        = None
#         self.base_folder   = '/tmp/tmp-input'
#         self.target_file   = f'{self.base_folder}/doc-1.docx.zip'
#         self.target_folder = f'{self.base_folder}/bbbb.docx'
#
#     def tearDown(self) -> None:
#         if self.result is not None:
#             Dev.pprint(self.result)
#
#     def test_zip_File(self):
#         with Unzip_File(self.target_file, self.target_folder, delete_target_folder=False):
#             with Zip_Folder(self.target_folder, delete_zip_file=False):
#                 self.result = 'alldone'
#
#     def test_just_unzip_File(self):
#         with Unzip_File(self.target_file, self.target_folder, delete_target_folder=False):
#             self.result = 'done'
#
#     def test_just_zip(self):
#         with Zip_Folder(self.target_folder, delete_zip_file=False):
#             self.result = 'alldone'
#
#
#     def test_parse_sisl(self):
#         path_sisl = '/tmp/tmp-input/bbbb.docx/Id_192233350_container_9.sisl'
#         path_sisl = '/tmp/tmp-input/bbbb.docx/Id_192233350_stream_1.sisl'
#         path_json = f'{path_sisl}.json'
#         content = Files.contents(path_sisl)
#
#         tag_names   = ['FileStream','DOCUMENT','STRUCTARRAY', 'VALUEARRAY',
#                        'STRUCT','VALUE',
#                        'ITEM']
#         field_names = ['cameraname','streamname', '__children',
#                        'name', 'estrc','offset','size', 'eitem',
#                        '__data']
#
#         mappings = [    ('__struct'      , '"__struct'     ),
#                         ('__meta: !__'   , '"meta":'       )]
#
#         for tag_name in tag_names:
#             mappings.append((f'!{tag_name}', f'{tag_name}":'))
#
#         for field_name in field_names:
#             mappings.append((f'{field_name}: !__', f'"{field_name}":'))
#
#         json_data = ""
#         for line in content.splitlines():
#             for key, value in mappings:
#                 line = line.replace(key,value)
#             json_data += f'{line}\n'
#
#         Files.write(path_json, json_data)           # save to disk
#         json.loads(json_data)                       # confirm load
#
#         # print(json_data)
#         #Json.load_json(path)
#
#     def test_edit_sisl(self):
#         path_json = '/tmp/tmp-input/bbbb.docx/Id_192233350_stream_5.sisl.json'
#         json_data = Json.load_json(path_json)
#         json_data["__struct_620: VALUEARRAY"]['__data'] = 'Changed from Python'
#         Dev.pprint(json_data["__struct_620: VALUEARRAY"]['__data'])
#
#         Json.save_json_pretty(path_json, json_data)
#
#     def test_write_sisl(self):
#         path_json = '/tmp/tmp-input/bbbb.docx/Id_192233350_stream_5.sisl.json'
#         path_sisl = '/tmp/tmp-input/bbbb.docx/Id_192233350_stream_5.sisl.json.sisl'
#         json_data = Files.contents(path_json)
#
#         tag_names = ['FileStream', 'DOCUMENT', 'STRUCTARRAY', 'VALUEARRAY',
#                      'STRUCT', 'VALUE',
#                      'ITEM']
#
#         field_names = ['cameraname', 'streamname', '__children',
#                        'name', 'estrc', 'offset', 'size', 'eitem',
#                        '__data']
#
#         mappings = [('"__struct', '__struct'    ),
#                     ('"meta":'  , '__meta: !__' )]
#
#         for tag_name in tag_names:
#             mappings.append((f'{tag_name}":', f'!{tag_name}'))
#
#         for field_name in field_names:
#             mappings.append((f'"{field_name}":', f'{field_name}: !__'))
#
#         sisl_data = ""
#         for line in json_data.splitlines():
#             for key, value in mappings:
#                 line = line.replace(key, value)
#             sisl_data += f'{line}\n'
#
#         Files.write(path_sisl, sisl_data)




