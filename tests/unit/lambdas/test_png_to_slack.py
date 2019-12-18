import base64
import unittest

from pbx_gs_python_utils.utils.Dev import Dev
from osbot_aws.apis.Lambda import Lambda

from gw_bot.Deploy import Deploy


class Test_Lambda_pdf_to_slack(unittest.TestCase):
    def setUp(self):
        self.png_to_slack = Lambda('utils.png_to_slack')

    def test_update_and_invoke(self):
        deploy = Deploy()
        deploy.oss_setup.setup_test_environment()
        deploy.deploy_lambda_png_to_slack()

        png_file = '/tmp/lambda_png_file.png'
        png_data = base64.b64encode(open(png_file, 'rb').read()).decode()
        Dev.pprint(len(png_data))
        payload   = { "png_data": png_data, 'aws_secrets_id':'slack-gs-bot', 'channel': 'DRE51D4EM'}

        result = self.png_to_slack.invoke(payload)

        Dev.pprint(result)