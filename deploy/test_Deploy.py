
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper


class test_Deploy(Test_Helper):

    def setUp(self):
        super().setUp()
        self.deploy = Deploy()
        #self.deploy.oss_setup.setup_test_environment()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_deploy_lambda__oss_bot(self):
        self.deploy.deploy_lambda__gw_bot()

    def test_deploy_lambda__browser(self):
        self.result = self.deploy.deploy_lambda__browser()

    def test_deploy_lambda__slack_message(self):
        result = self.deploy.deploy_lambda__slack_message()
        Dev.pprint(result)

    def test_deploy_lambda_log_to_elk(self):
        lambda_package = self.deploy.deploy_lambda_log_to_elk()
        self.result  = lambda_package._lambda.invoke()


    # def test_lambda_browser(self):
    #     self.test_deploy_lambda__browser()
    #     from osbot_aws.apis.Lambda import Lambda
    #     self.result = Lambda('osbot_browser.lambdas.lambda_browser').invoke({})


    def test_deploy_browser_jira_web(self):
        self.deploy.deploy_lambda__browser('osbot_browser.lambdas.jira_web')