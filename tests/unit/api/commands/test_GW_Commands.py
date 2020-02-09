from gw_bot.lambdas.gw_bot import run
from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from gw_bot.api.commands.GW_Commands import GW_Commands
from gw_bot.helpers.Test_Helper import Test_Helper


class test_OSS_Bot_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_ping(self):
        self.result = GW_Commands.ping()

    def test_api_usage(self):
        self.result = GW_Commands.api_usage(channel='DRE51D4EM')

    def test_api_keys(self):
        self.result = GW_Commands.api_keys()

    def test_update_lambda(self):
        Deploy().deploy_lambda__gw_bot()

    def test_invoke_directly(self):
        payload = {'event': {'type': 'message', 'text': 'gw api_usage', 'channel':'DRE51D4EM'}}
        self.result = run(payload,None)

    def test_invoke_lambda(self):
        self.test_update_lambda()
        payload = {'event': {'type': 'message', 'text': 'gw api_usage'}}
        self.result = Lambda('gw_bot.lambdas.gw_bot').invoke(payload)

