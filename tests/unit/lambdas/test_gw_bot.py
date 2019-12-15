from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.Lambdas import Lambdas
from osbot_aws.helpers.Lambda_Package import Lambda_Package

from gw_bot.helpers.Test_Helper import Test_Helper


class test_run_command(Test_Helper):
    def setUp(self):
        #self.oss_setup = super().setUp()
        #self.aws_lambda = Lambda_Package('gw_bot.lambdas.gw_bot')
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw_bot')
        #self.aws_lambda._lambda.set_s3_bucket(self.oss_setup.s3_bucket_lambdas)         \
        #                       .set_role     (self.oss_setup.role_lambdas)
        #self.aws_lambda.create()  # use when wanting to update lambda function

    def update_lambda(self):
        self.aws_lambda.update_code()

    def test__invoke_directy(self):
        from gw_bot.lambdas.gw_bot import run
        self.result = run({'event': {'type': 'message', 'text': 'help'}},{})

    def test_invoke(self):
        self.update_lambda()
        self.result = self.aws_lambda.invoke({'event': {'type': 'message', 'text': 'help'}})

    def test_invoke_with_channel(self):
        self.update_lambda()
        self.result = self.aws_lambda.invoke({'event': {'type': 'message', 'text': 'help', "channel": "DRE51D4EM"}})

    def test_participant_view(self):
        self.update_lambda()
        text = 'participant view Dinis Cruz'
        self.result = self.aws_lambda.invoke({'event': {'type': 'message', 'text': text, "channel": "DJ8UA0RFT"}})