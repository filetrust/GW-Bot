from gw_bot.lambdas.gw_bot import run
from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from gw_bot.api.commands.gw.GW_Commands import GW_Commands
from gw_bot.helpers.Test_Helper import Test_Helper


class test_OSS_Bot_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.result = None

    def test_ping(self):
        self.result = GW_Commands.ping()


    def test_update_lambda(self):
        Deploy().deploy_lambda__gw_bot('gw_bot.lambdas.gw.commands')

    def test_invoke_directly(self):
        payload = {'event': {'type': 'message', 'text': 'gw api_usage', 'channel':'DRE51D4EM'}}
        self.result = run(payload,None)

    def test_invoke_lambda(self):
        self.test_update_lambda()
        payload = {'event': {'type': 'message', 'text': 'gw api_usage'}}
        self.result = Lambda('gw_bot.lambdas.gw_bot').invoke(payload)

