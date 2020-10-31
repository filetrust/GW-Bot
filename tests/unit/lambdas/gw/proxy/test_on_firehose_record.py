from osbot_aws.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.gw.proxy.on_firehose_record import run


class test_saas_vps(Test_Helper):

    def setUp(self):
        super().setUp()
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw.proxy.on_firehose_record')

    def test_update_lambda(self):
        self.aws_lambda.update_code()
        #self.result = self.aws_lambda.arn()

    def test__invoke_directy(self):
        #payload = {'path':'/favicon-shard.png'}
        payload = {}
        self.result = run(payload)

    def test_invoke(self):
        self.aws_lambda.update_code()
        self.result = self.aws_lambda.invoke({})
