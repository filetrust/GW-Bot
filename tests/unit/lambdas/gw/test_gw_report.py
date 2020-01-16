from unittest import TestCase

from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.gw.gw_report import run
from unit.api.gw.test_Report_Xml_Parser import test_Report_Xml_Parser


class test_gw_report(Test_Helper):

    def setUp(self):
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw.gw_report')

    def test_update_lambda(self):
        self.aws_lambda.update_code()

    def test__invoke_directy(self):
        xml_report = test_Report_Xml_Parser().tmp_xml_report('macros.xml-report.xml')
        payload = {'xml_report' : xml_report}
        self.result = run(payload,{})

    def test__invoke_via_lambda(self):
        #self.test_update_lambda()
        xml_report = test_Report_Xml_Parser().tmp_xml_report('macros.xml-report.xml')
        payload = {'xml_report': xml_report}
        self.result = self.aws_lambda.invoke(payload)

class Test_Using_Lambda_API(Test_Helper):
    def test__invoke_via_lambda(self):
        xml_report = test_Report_Xml_Parser().tmp_xml_report('macros.xml-report.xml')
        payload = {'xml_report': xml_report}
        #self.result = self.aws_lambda.invoke(payload)

        from osbot_aws.apis.Lambda import Lambda
        from pbx_gs_python_utils.utils.Dev import Dev
        result = Lambda('gw_bot.lambdas.gw.gw_report').invoke(payload)
        Dev.pprint(result)

