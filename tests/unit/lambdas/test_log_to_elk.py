#from osbot_aws.Dependencies import upload_dependency
from osbot_aws.apis.Lambda import Lambda
from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.log_to_elk import run
from osbot_utils.utils.Dev import Dev


class Test_Lambda_log_to_elk(Test_Helper):
    def setUp(self):
        super().setUp()
        self.log_to_elk = Lambda('gw_bot.lambdas.log_to_elk')
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_invoke_directly(self):
        payload = {}
        self.result = run(payload, {})
    # def test_update_invoke(self):
    #     payload = {'message' : 'an message'}
    #     response = self.log_to_elk.update_with_lib().invoke(payload)
    #
    #     Dev.pprint(response)
    #     #assert response.get('elastic_response').get('result') == 'created'
    #
    #     #assert self.log_to_elk.update_with_lib().invoke({}) is None

    def test_invoke___check_multiple_log_options(self):
        response = self.log_to_elk.invoke({ 'level': 'info' , 'category': 'category info' , 'message': 'message info' , 'data': {'answer' : 42}})
        assert response.get('elastic_response').get('result') == 'created'
        response = self.log_to_elk.invoke({ 'level': 'debug', 'category': 'category debug', 'message': 'message debug', 'data': {'answer' : 42}})
        assert response.get('elastic_response').get('result') == 'created'
        response = self.log_to_elk.invoke({ 'level': 'error', 'category': 'category error', 'message': 'message error', 'data': {'answer' : 42}})
        assert response.get('elastic_response').get('result') == 'created'


    # def test_upload_dependency(self):
    #     upload_dependency("elastic")

        #pip3 install elasticsearch -t elastic