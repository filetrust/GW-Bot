from osbot_aws.apis.Lambda import Lambda
from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.Deploy import Deploy

class test_slack_message(Test_Helper):
    def setUp(self):
        self.oss_setup = super().setUp()
        self.aws_lambda = Lambda('pbx_gs_python_utils_lambdas_utils_slack_message')

    def test_update_lambda(self):
        Deploy().deploy_lambda__slack_message()

    def test_invoke(self):
        self.test_update_lambda()
        channel = 'DRE51D4EM' # gw_bot
        payload = {
            'text': 'this is a text',
            'attachments': [{'text': 'an attach', 'color':'good'}],
            'channel': channel
        }
        self.result = self.aws_lambda.invoke(payload)


