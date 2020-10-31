from gw_bot.lambdas.gw.store.create_api_gw_api_key import run
from osbot_aws.apis.Lambda import Lambda

from gw_bot.Deploy import Deploy
from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_aws.helpers.Rest_API import Rest_API


class test_run_command(Test_Helper):
    def setUp(self):
        super().setUp()
        self.lambda_name = 'gw_bot.lambdas.gw.store.create_api_gw_api_key'
        self.api_name    = 'api-key-generator-for-shopify'
        self.aws_lambda  = Lambda(self.lambda_name)
        self.rest_api    = Rest_API(self.api_name)

    def test_update_lambda(self):
        Deploy().deploy_lambda__gw_bot(self.lambda_name)

    def test_invoke_directly(self):
        self.result = run({},{})

    def test_invoke_directly_with_params(self):
        payload = {'queryStringParameters' :{'order_id': '1234', 'product_id': '', 'product_name': 'File Type Detection - 50 (Free)', 'product_variant': '32131192029324', 'signature': 'L7sJDEbz6LZD++JsY2M8RYNv7+g='} }
        self.result = run(payload, {})

    def test_invoke_lambda(self):
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke({})


    # setup API GW route to lambda
    def test_setup_lambda_route(self):
        name        = 'api-key-generator-for-shopify'
        lambda_name = 'gw_bot_lambdas_gw_store_create_api_gw_api_key'
        rest_api    = Rest_API(name).create()

        rest_api.add_method_lambda('/','GET',lambda_name)
        rest_api.deploy()
        self.result = rest_api.test_method('/','GET')

    def test_invoke_rest_api(self):
        self.test_update_lambda()
        #self.result = self.rest_api.url()
        self.result = self.rest_api.invoke_GET('?abc=123')

