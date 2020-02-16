# create REST API that creates a proxy for multiple sites
from pbx_gs_python_utils.utils.Http import GET

from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.gw.proxy.saas_vps import run
from osbot_aws.helpers.Rest_API import Rest_API

class test_saas_vps(Test_Helper):

    def setUp(self):
        super().setUp()
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw.proxy.saas_vps')

    def test_update_lambda(self):
        self.aws_lambda.update_code()

    def test__invoke_directy(self):
        payload = {}
        self.result = run(payload, {})

    def test__invoke_via_lambda(self):
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke()


class test_Rest_API__SaaS_VPs(Test_Helper):

    def setUp(self):
        super().setUp()
        self.api_name    = 'lambda-proxy'
        self.lambda_name = 'gw_bot_lambdas_gw_proxy_saas_vps'

    def test_setup_lambda_route(self):

        rest_api    = Rest_API(self.api_name).create()
        rest_api.add_method_lambda('/','GET',self.lambda_name)
        rest_api.deploy()
        self.result = rest_api.test_method('/','GET')

    def test_GET_request(self):
        self.result = GET(Rest_API(self.api_name).url())