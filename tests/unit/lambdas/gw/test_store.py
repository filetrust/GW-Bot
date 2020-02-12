from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.gw.store import run


class test_gw_engine(Test_Helper):
    def setUp(self):
        super().setUp()
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw.store')
        self.params = {'data' : {'channel': 'DRE51D4EM'}}

    def test_update_lambda(self):
        self.aws_lambda.update_code()

    def test_invoke_directy(self):
        self.result = run(self.params, None)

    def test_invoke_directy__keys(self):
        self.result = run({'params': ['keys']}, None)

    def test_invoke_via_lambda(self):
        #self.test_update_lambda()
        self.result = self.aws_lambda.invoke(self.params)

    def test_invoke_via_lambda_ping(self):
        self.result = self.aws_lambda.invoke({'params': ['ping']})

    def test_invoke_via_lambda__keys_list(self):
        #self.test_update_lambda()
        self.result = self.aws_lambda.invoke({'params': ['keys','list']})

    def test_invoke_via_lambda__keys_usage(self):
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke({'params': ['keys','usage']})

    def test_bug(self):
        self.result = run({'params': ['ping']},{})