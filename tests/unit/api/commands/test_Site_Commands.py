from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.api.commands.Site_Commands import Site_Commands
from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.Deploy import Deploy

class test_OSS_Bot_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_home_page(self):
        self.test_deploy_lambda__oss_bot()
        self.site_result = Site_Commands().home_page(None, 'CJ91NQX17')

    def test_page_404(self):
        self.result = Site_Commands().page_404(None, 'CJ91NQX17',[])
        print(self.result)

    def test_abc(self):
        self.result = Site_Commands().abc(None, 'CJ91NQX17')

    def test_deploy_lambda__browser(self):
        package = Deploy().setup().deploy_lambda__browser()
        self.result = package._lambda.invoke()

    def test_deploy_lambda__oss_bot(self):
        package = Deploy().setup().deploy_lambda__oss_bot()
        self.result = package._lambda.invoke()