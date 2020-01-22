from unittest import TestCase

from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.gw.gw_slack_file import run


class test_gw_report(Test_Helper):

    def setUp(self):
        super().setUp()
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw.gw_slack_file')
        self.payload    = { "type"    : "file_created",
                            "file"    : {"id": "FSWQ0UYGP"},
                            "file_id" : "FSWQ0UYGP",
                            "user_id" : "URS8QH4UF",
                            "event_ts": "1579473069.000200"}

    def test_update_lambda(self):
        self.aws_lambda.update_code()

    def test__invoke_directy(self):
        self.result = run(self.payload,{})

    def test__update_and_invoke_via_lambda(self):
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke(self.payload)

    def test__invoke_via_lambda(self):
        self.result = self.aws_lambda.invoke(self.payload)
