from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.gw.gw_engine import run


class test_gw_engine(Test_Helper):
    def setUp(self):
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw.gw_engine')

    def test_update_lambda(self):
        self.aws_lambda.update_code()

    def test__invoke_directy(self):
        self.result = run({'event': {'type': 'message', 'text': 'help'}},{})

    def test__invoke_via_lambda(self):
        #self.test_update_lambda()
        self.result = self.aws_lambda.invoke()
