from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.api.commands.GW_Commands import GW_Commands
from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_browser.Deploy import Deploy


class test_OSS_Bot_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_ping(self):
        self.result = GW_Commands.ping()

    def test_get_test_list(self):
        self.result = GW_Commands.get_test_list()


    def test_deploy_lambda__gw_bot(self):
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw_bot')
        self.aws_lambda.update_code()

