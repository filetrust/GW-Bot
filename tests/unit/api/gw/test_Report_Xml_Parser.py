from unittest import TestCase

from pbx_gs_python_utils.utils import Http
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files

from gw_bot.api.gw.Report_Xml_Parser import Report_Xml_Parser


class test_Report_Xml_Parser(TestCase):

    def setUp(self):
        self.parser     = Report_Xml_Parser()
        self.result     = None
        self.xml_report = self.tmp_xml_report()

    def tearDown(self):
        if self.result:
            Dev.print(self.result)

    def tmp_xml_report(self):
        name     = 'macros.xml-report.xml'
        tmp_path = f'/tmp/{name}'
        path     = f'https://raw.githubusercontent.com/filetrust/GW-Test-Files/master/xml-reports/{name}'
        if Files.not_exists(tmp_path):
            file_contents = Http.GET(path)
            Files.write(tmp_path, file_contents)
        else:
            file_contents = Files.contents(tmp_path)
        return file_contents

    def test_confirm_temp_xml_report_exists(self):
        assert '<?xml version="1.0" encoding="utf-8"?>' in self.xml_report
