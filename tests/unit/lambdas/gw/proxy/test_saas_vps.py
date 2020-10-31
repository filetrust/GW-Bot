# create REST API that creates a proxy for multiple sites

from osbot_aws.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.gw.proxy.saas_vps import run
from osbot_aws.apis.API_Gateway import API_Gateway
from osbot_aws.helpers.Rest_API import Rest_API

class test_saas_vps(Test_Helper):

    def setUp(self):
        super().setUp()
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw.proxy.saas_vps')

    def test_update_lambda(self):
        self.aws_lambda.update_code()

    def test__invoke_directy(self):
        #payload = {'path':'/favicon-shard.png'}
        payload = {'path': '/', 'httpMethod': 'GET', 'headers': {'aaa': 'bbbb'}}
        self.result = run(payload, {})

    def test__invoke_directy__glasswall(self):
        payload = {'path': '/', 'httpMethod': 'GET', 'headers': {}, 'requestContext': {'domainPrefix': 'glasswall'} }
        self.result = run(payload, {})

    def test__invoke_directy__send_firefox_com(self):
        payload = {'path': '/', 'httpMethod': 'GET', 'headers': {}, 'requestContext': {'domainPrefix': 'send_firefox_com'}}
        self.result = run(payload, {})

    def test__invoke_via_lambda(self):
        #payload = {'path': '/favicon-shard.png'}
        payload = {'path': '/', 'httpMethod': 'GET', 'headers': {'aaa': 'bbbb'}}
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke(payload)
        #self.png_data = self.result.get('body')

    def test__invoke_via_lambda__glasswall(self):
        #payload = {'path': '/wp-content/uploads/2019/12/deepfile-340.png', 'requestContext': {'domainPrefix': 'glasswall'}}
        payload = {'path': '/', 'httpMethod': 'GET', 'headers': {'aaa': 'bbbb'}, 'requestContext': {'domainPrefix': 'glasswall'} }
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke(payload)

    # def test_invoke_directly_with_payload(self):
    #     payload = {'resource': '/', 'path': '/', 'httpMethod': 'GET', 'headers': {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-GB,en;q=0.9,pt-PT;q=0.8,pt;q=0.7,en-US;q=0.6', 'Host': 'gw-proxy.com', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36', 'X-Amzn-Trace-Id': 'Root=1-5e48be59-9bbf9c36970c2c503b01ae20', 'X-Forwarded-For': '82.39.36.190', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'], 'accept-encoding': ['gzip, deflate, br'], 'accept-language': ['en-GB,en;q=0.9,pt-PT;q=0.8,pt;q=0.7,en-US;q=0.6'], 'Host': ['gw-proxy.com'], 'sec-fetch-mode': ['navigate'], 'sec-fetch-site': ['none'], 'sec-fetch-user': ['?1'], 'upgrade-insecure-requests': ['1'], 'User-Agent': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'], 'X-Amzn-Trace-Id': ['Root=1-5e48be59-9bbf9c36970c2c503b01ae20'], 'X-Forwarded-For': ['82.39.36.190'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'g72apoktf2', 'resourcePath': '/', 'httpMethod': 'GET', 'extendedRequestId': 'H-KuBFP3joEFiuQ=', 'requestTime': '16/Feb/2020:04:00:25 +0000', 'path': '/', 'accountId': '311800962295', 'protocol': 'HTTP/1.1', 'stage': 'Prod', 'domainPrefix': 'gw-proxy', 'requestTimeEpoch': 1581825625683, 'requestId': '3ff4b3e5-5503-4750-9ef5-cf61b888d552', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '82.39.36.190', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36', 'user': None}, 'domainName': 'gw-proxy.com', 'apiId': 'l2zujsuve3'}}
    #     self.result = run(payload,{})
    #
    # def test_invoke_directly__GET_root_path(self):
    #     payload = { 'path': '/aaa', 'httpMethod': 'GET', 'headers': {'accept': 'text/html,application/xhtml+xml,application/xml'}}
    #     self.result = run(payload)








# this call and methods contain the multiple bits required to set up the proxy (todo: consolidate in one end-to-end solution to be executed on a clear AWS region/organisation)
class test_Rest_API__SaaS_VPs(Test_Helper):

    def setUp(self):
        super().setUp()
        self.api_name    = 'lambda-proxy'
        self.lambda_name = 'gw_bot_lambdas_gw_proxy_saas_vps'
        self.api_gateway = API_Gateway()

    def test_setup_lambda_route(self):                      # will create a {proxy+} integration
        rest_api    = Rest_API(self.api_name).create()
        parent_id = rest_api.resource_id('/')
        rest_api.api_gateway.resource_create(rest_api.id(),parent_id,'{proxy+}')
        self.result = rest_api.add_method_lambda('/'        , 'ANY', self.lambda_name)  # need to add both
        self.result = rest_api.add_method_lambda('/{proxy+}', 'ANY', self.lambda_name)  # since this one wasn't catching the root requests
        rest_api.deploy()
        #self.result = rest_api.test_method('/','GET')

    def test_deploy_api(self):
        rest_api = Rest_API(self.api_name).create()
        self.result = rest_api.deploy()

    # here is the test that added the A record for both top level domain and child domains
    # def test_record_set_upsert(self):
    #
    #     name                = 'gw-proxy.com.'
    #     record_type         = 'A'
    #     dns_name            = 'd-noho75bpih.execute-api.eu-west-1.amazonaws.com.'
    #     hosted_zone_id      = '/hostedzone/ZMHOWKWA1ZN69'
    #     alias_hosted_zone_id = 'ZLY8HYME6SFDD'
    #     self.result = Route_53().record_set_upsert(name, record_type, dns_name,hosted_zone_id,alias_hosted_zone_id)
    #
    # def test_record_set_upsert(self):
    #     from osbot_aws.apis.Route_53 import Route_53
    #     name                = '*.gw-proxy.com.'
    #     record_type         = 'A'
    #     dns_name            = 'd-noho75bpih.execute-api.eu-west-1.amazonaws.com.'
    #     hosted_zone_id      = '/hostedzone/ZMHOWKWA1ZN69'
    #     alias_hosted_zone_id = 'ZLY8HYME6SFDD'
    #     self.result = Route_53().record_set_upsert(name, record_type, dns_name,hosted_zone_id,alias_hosted_zone_id)
    #
    # # here is the test that asked for the wildcart Cert to be created
    # def test_certificate_request(self):
    #     #self.result = self.acm.certificate_request('*.gw-proxy.com')
    #     self.result = self.acm.certificate('arn:aws:acm:eu-west-1:311800962295:certificate/1f191c3a-0214-4ef5-9f03-27cc0b46bef3')
    #
    # def test_GET_request(self):
    #     self.result = GET(Rest_API(self.api_name).url())
    #
    # # adding domain to API Gateway
    # # gw-proxy.com
    # def test_domain_name_add_path_mapping(self):
    #     rest_api_id = self.api_gateway.rest_api_id('lambda-proxy')
    #     domain_name = 'gw-proxy.com'
    #     base_path   = ''
    #     self.result = self.api_gateway.domain_name_add_path_mapping(rest_api_id=rest_api_id,domain_name=domain_name,base_path=base_path)
    #
    # def test_domain_name_create(self):
    #     domain_name     = 'gw-proxy.com'
    #     certificate_arn = 'arn:aws:acm:eu-west-1:311800962295:certificate/cac6ccbe-e5a6-41b1-ab87-461ff1d88458'
    #     self.result     = self.api_gateway.domain_name_create__regional(domain_name=domain_name, certificate_arn=certificate_arn)
    #
    # # *.gw-proxy.com
    #
    # def test_domain_name_create(self):
    #     domain_name     = '*.gw-proxy.com'
    #     certificate_arn = 'arn:aws:acm:eu-west-1:311800962295:certificate/be75edef-b698-4425-bf7a-7a129bb0331e'
    #     self.result     = self.api_gateway.domain_name_create__regional(domain_name=domain_name, certificate_arn=certificate_arn)
    #
    # def test_domain_name_add_path_mapping(self):
    #     rest_api_id = self.api_gateway.rest_api_id('lambda-proxy')
    #     domain_name = '*.gw-proxy.com'
    #     base_path   = ''
    #     self.result = self.api_gateway.domain_name_add_path_mapping(rest_api_id=rest_api_id,domain_name=domain_name,base_path=base_path)
