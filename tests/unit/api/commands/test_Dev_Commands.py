from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from gw_bot.api.commands.Dev_Commands import Dev_Commands
from gw_bot.helpers.Test_Helper import Test_Helper

class test_Dev_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_slack_name(self):
        #self.test_deploy_lambda__oss_bot()
        self.result = Dev_Commands().slack_name('UAULZ1T98',None, None)

        # deploy helpers

    def test_deploy_lambda__oss_bot(self):
        Deploy().setup().deploy_lambda__oss_bot()




