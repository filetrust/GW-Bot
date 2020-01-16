from unittest import TestCase

from pbx_gs_python_utils.utils import Http
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files

from gw_bot.api.gw.Report_Xml_Parser import Report_Xml_Parser


class test_Report_Xml_Parser(TestCase):

    def setUp(self):
        self.result     = None
        self.test_file  = 'macros.xml-report.xml'
        #self.test_file = 'png-file-report.xml'
        self.xml_report = self.tmp_xml_report(self.test_file)
        self.parser     = Report_Xml_Parser(self.xml_report)

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

    # internal test documents
    def tmp_xml_report(self, file_name):
        tmp_path = f'/tmp/{file_name}'
        path     = f'https://raw.githubusercontent.com/filetrust/GW-Test-Files/master/xml-reports/{file_name}'
        if Files.not_exists(tmp_path):
            file_contents = Http.GET(path)
            Files.write(tmp_path, file_contents)
        else:
            file_contents = Files.contents(tmp_path)
        return file_contents

    # helper methods
    def test_remove_namespace_references(self):
        assert self.parser.root().tag == 'GWallInfo'            # without the remove function this value would be "{http://glasswall.com/namespace}GWallInfo"

    def test_confirm_temp_xml_report_exists(self):
        assert '<?xml version="1.0" encoding="utf-8"?>' in self.xml_report

    # ctor

    def test_ctor(self):
        assert len(self.parser.report_xml) == 52543
        assert self.parser.config == {'include_content_groups': True, 'include_policy': True}

    # element methods

    def test_content_content_management_policy(self):
        assert self.parser.content_content_management_policy().tag                  == 'ContentManagementPolicy'

    def test_content_groups(self):
        assert self.parser.content_groups().tag                  == 'ContentGroups'
        assert self.parser.content_groups().attrib['groupCount'] == '17'

    def test_extracted_items(self):
        assert self.parser.extracted_items().tag                 == 'ExtractedItems'
        assert self.parser.extracted_items().attrib['itemCount'] == '0'

    # Parse methods

    def test_parse_Document_Summary(self):
        assert self.parser.parse_document_summary() == {'TotalSizeInBytes': '0', 'FileType': 'xls', 'Version': 'Not Applicable'}

    def test_parse_Content_Management_Policy(self):
        result = self.parser.parse_content_management_policy()
        assert list(result.keys()) == ['pdfConfig', 'wordConfig', 'pptConfig', 'xlsConfig']
        assert result['pdfConfig'] == { 'acroform'       : 'sanitise', 'actions_all'        : 'sanitise', 'embedded_files'     : 'sanitise' ,
                                        'embedded_images': 'sanitise', 'external_hyperlinks': 'sanitise', 'internal_hyperlinks': 'sanitise' ,
                                        'javascript'     : 'sanitise', 'metadata'           : 'sanitise'                                    }


    #def test_parse_content_groups(self):
    #    self.result = self.parser.parse_content_groups()

    def test_parse_document(self):
        config = {
                    "include_policy"            : False,
                    "include_content_groups"    : True ,
                    "include_content_items"     : True,
                    "include_issue_items"       : True,
                    "include_remedy_items"      : True,
                    "include_sanitisation_items": True
                }
        #self.parser.config = False
        result = self.parser.set_config(config).parse_document()
        self.result = result

    def test_root(self):
        assert self.parser.root().tag     == 'GWallInfo'
        assert len(self.parser.root())    == 1
        assert len(self.parser.root()[0]) == 4
