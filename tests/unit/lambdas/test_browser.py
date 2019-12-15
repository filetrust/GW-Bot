import base64
from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.Lambdas import Lambdas
from osbot_aws.apis.Secrets import Secrets
from osbot_aws.helpers.Lambda_Package import Lambda_Package
from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper


class test_run_command(Test_Helper):
    def setUp(self):
        self.oss_setup  = super().setUp()
        self.aws_lambda = Lambda('osbot_browser.lambdas.lambda_browser')
        self.result     = None
        self.png_data   = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)
        if self.png_data:
            png_file = '/tmp/lambda_png_file.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))

    def test__invoke__directly(self):
        from osbot_browser.lambdas.lambda_browser import run
        self.result = run({},{})

    def test__invoke__no_params(self):
        assert self.aws_lambda.invoke() == '*Here are the `Browser_Commands` commands available:*'

    def test__invoke__version(self):
        payload = { "params" :["version"]}
        self.result = self.aws_lambda.invoke(payload)

    def test__invoke__screenshot(self):
        deploy = Deploy()
        deploy.oss_setup.setup_test_environment()
        deploy.deploy_lambda__browser()
        payload = {"params": ["screenshot", "https://www.google.com/images", "1200"],
                   'data': {'channel': 'DJ8UA0RFT'}}
        self.result = self.aws_lambda.invoke(payload)
        #self.png_data = self.aws_lambda.invoke(payload)

    def test__invoke__screenshot__no_channel(self):
        deploy = Deploy()
        deploy.oss_setup.setup_test_environment()
        deploy.deploy_lambda__browser()
        payload = {"params": ["screenshot", "https://www.google.com/images"]}
        self.result = self.aws_lambda.invoke(payload)
