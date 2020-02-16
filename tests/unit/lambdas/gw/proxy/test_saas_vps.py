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
        #payload = {'path':'/favicon-shard.png'}
        payload = {'path': '/'}
        self.result = run(payload, {})

    def test__invoke_via_lambda(self):
        payload = {'path': '/favicon-shard.png'}
        payload = {'path': ''}
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke(payload)
        #self.png_data = self.result.get('body')

    def test_invoke_directly_with_payload(self):
        payload = {'resource': '/', 'path': '/', 'httpMethod': 'GET', 'headers': {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-GB,en;q=0.9,pt-PT;q=0.8,pt;q=0.7,en-US;q=0.6', 'Host': 'gw-proxy.com', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36', 'X-Amzn-Trace-Id': 'Root=1-5e48be59-9bbf9c36970c2c503b01ae20', 'X-Forwarded-For': '82.39.36.190', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'], 'accept-encoding': ['gzip, deflate, br'], 'accept-language': ['en-GB,en;q=0.9,pt-PT;q=0.8,pt;q=0.7,en-US;q=0.6'], 'Host': ['gw-proxy.com'], 'sec-fetch-mode': ['navigate'], 'sec-fetch-site': ['none'], 'sec-fetch-user': ['?1'], 'upgrade-insecure-requests': ['1'], 'User-Agent': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'], 'X-Amzn-Trace-Id': ['Root=1-5e48be59-9bbf9c36970c2c503b01ae20'], 'X-Forwarded-For': ['82.39.36.190'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'g72apoktf2', 'resourcePath': '/', 'httpMethod': 'GET', 'extendedRequestId': 'H-KuBFP3joEFiuQ=', 'requestTime': '16/Feb/2020:04:00:25 +0000', 'path': '/', 'accountId': '311800962295', 'protocol': 'HTTP/1.1', 'stage': 'Prod', 'domainPrefix': 'gw-proxy', 'requestTimeEpoch': 1581825625683, 'requestId': '3ff4b3e5-5503-4750-9ef5-cf61b888d552', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '82.39.36.190', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36', 'user': None}, 'domainName': 'gw-proxy.com', 'apiId': 'l2zujsuve3'}}
        self.result = run(payload,{})

    def test_invoke_directly__GET_root_path(self):
        payload = { 'path': '/aaa', 'httpMethod': 'GET', 'headers': {'accept': 'text/html,application/xhtml+xml,application/xml'}}
        self.result = run(payload)








class test_Rest_API__SaaS_VPs(Test_Helper):

    def setUp(self):
        super().setUp()
        self.api_name    = 'lambda-proxy'
        self.lambda_name = 'gw_bot_lambdas_gw_proxy_saas_vps'

    def test_setup_lambda_route(self):                      # will create a {proxy+} integration
        rest_api    = Rest_API(self.api_name).create()
        parent_id = rest_api.resource_id('/')
        rest_api.api_gateway.resource_create(rest_api.id(),parent_id,'{proxy+}')
        self.result = rest_api.add_method_lambda('/'        , 'ANY', self.lambda_name)  # need to add both
        self.result = rest_api.add_method_lambda('/{proxy+}', 'ANY', self.lambda_name)  # since this one wasn't catching the root requests
        rest_api.deploy()
        #self.result = rest_api.test_method('/','GET')

    def test_add_proxy_route(self):
        rest_api = Rest_API(self.api_name)
        rest_api_id = rest_api.id()
        parent_id = rest_api.resource_id('/')
        #rest_api.api_gateway.resource_create(rest_api_id,parent_id,'{proxy+}')
        #self.result = rest_api.add_method_lambda('/{proxy+}', 'ANY', self.lambda_name)
        rest_api.deploy()
        # self.result = rest_api_id.add_method_lambda('/', '{proxy+}')
        #self.result = rest_api.api_gateway.resources(rest_api_id)



    def test_GET_request(self):
        self.result = GET(Rest_API(self.api_name).url())