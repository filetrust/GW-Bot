from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.Lambdas import Lambdas
from osbot_aws.helpers.Lambda_Package import Lambda_Package

from gw_bot.helpers.Test_Helper import Test_Helper


class test_slack_message(Test_Helper):
    def setUp(self):
        self.oss_setup = super().setUp()
        self.aws_lambda = Lambda('pbx_gs_python_utils_lambdas_utils_slack_message')

    def test_invoke(self):
        from gw_bot.Deploy import Deploy
        Deploy().deploy_lambda__slack_message()
        channel = 'DJ8UA0RFT' # gw_bot
        #API_OSS_Bot()
        payload = {
            'text': 'this is a text',
            'attachments': [{'text': 'an attach', 'color':'good'}],
            'channel': channel
        }
        self.result = self.aws_lambda.invoke(payload)


