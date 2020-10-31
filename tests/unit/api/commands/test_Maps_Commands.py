from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from gw_bot.api.commands.Maps_Commands import Maps_Commands
from osbot_aws.helpers.Test_Helper import Test_Helper

class test_Maps_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_ping(self):
        self.result = Maps_Commands().ping()

    def test_simple(self):
        self.test_deploy_lambda__oss_bot()
        self.result = Maps_Commands().simple(None, 'DJ8UA0RFT')

    def test_deploy_lambda__oss_bot(self):
        Deploy().setup().deploy_lambda__gw_bot()

    def test_deploy_lambda__browser(self):
        Deploy().setup().deploy_lambda__browser()




