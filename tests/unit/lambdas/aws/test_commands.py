from osbot_aws.helpers.Test_Helper import Test_Helper
#to do fix this reference
from gw_bot.lambdas.aws.commands import run


class test_commands(Test_Helper):
    def setUp(self):
        super().setUp()
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.aws.commands')
        self.params = {'data' : {'channel': 'DRE51D4EM'}}

    def test_update_lambda(self):
        self.aws_lambda.update_code()

    def test_invoke_directy(self):
        self.result = run(self.params, None)

    def test_invoke_directy__keys(self):
        self.result = run({'params': ['ping']}, None)

    def test_invoke_via_lambda(self):
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke(self.params)

    def test_invoke_via_lambda_ping(self):
        self.result = self.aws_lambda.invoke({'params': ['ping']})

    def test_invoke_via_lambda__billing(self):
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke({'params': ['billing'], 'channel': 'DRE51D4EM'})

    def test_bug(self):
        self.result = run({'params': ['ping']},{})