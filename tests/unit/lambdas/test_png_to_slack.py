import base64
import unittest

from pbx_gs_python_utils.utils.Dev import Dev
from osbot_aws.apis.Lambda import Lambda

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.png_to_slack import run


class Test_Lambda_pdf_to_slack(Test_Helper):
    def setUp(self):
        super().setUp()
        self.png_to_slack = Lambda('utils.png_to_slack')

    def test_update_lambda(self):
        Deploy().setup().deploy_lambda_png_to_slack()

    def test_invoke_directly(self):
        #self.test_update_lambda()
        png_file = '/tmp/lambda_png_file.png'
        png_data = base64.b64encode(open(png_file, 'rb').read()).decode()
        Dev.pprint(len(png_data))
        payload   = { "png_data": png_data, 'aws_secrets_id':'slack-gs-bot', 'channel': 'DRE51D4EM'}

        self.result = run(payload,{})


    def test_update_and_invoke(self):
        #self.test_update_lambda()
        png_file = '/tmp/lambda_png_file.png'
        png_data = base64.b64encode(open(png_file, 'rb').read()).decode()
        Dev.pprint(len(png_data))
        payload   = { "png_data": png_data, 'aws_secrets_id':'slack-gs-bot', 'channel': 'DRE51D4EM'}

        result = self.png_to_slack.invoke(payload)

        Dev.pprint(result)