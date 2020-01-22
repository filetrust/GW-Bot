from gw_bot.lambdas.gw_bot import run


from gw_bot.helpers.Test_Helper import Test_Helper


class test_run_command(Test_Helper):
    def setUp(self):
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw_bot')

    def update_lambda(self):
        self.aws_lambda.update_code()

    def test__invoke_directy(self):
        from gw_bot.lambdas.gw_bot import run
        self.result = run({'event': {'type': 'message', 'text': 'help'}},{})

    def test__invoke_directly_gw(self):
        self.result = run({'event': {'type': 'message', 'text': 'gw'}}, {})


    def test__invoke_directly_jira(self):
        self.result = run({'event': {'type': 'message', 'text': 'jira'}}, {})


    def test__invoke_directly_version(self):
        self.result = run({'event': {'type': 'message', 'text': 'version'}}, {})

    def test_invoke(self):
        self.update_lambda()
        self.result = self.aws_lambda.invoke({'event': {'type': 'message', 'text': 'help'}})

    def test_invoke_gw(self):
        self.update_lambda()
        self.result = self.aws_lambda.invoke({'event': {'type': 'message', 'text': 'gw'}})

    def test_invoke_version(self):
        self.update_lambda()
        self.result = self.aws_lambda.invoke({'event': {'type': 'message', 'text': 'version'}})

    def test_invoke_with_channel(self):
        self.update_lambda()
        self.result = self.aws_lambda.invoke({'event': {'type': 'message', 'text': 'help', "channel": "DRE51D4EM"}})

    def test_participant_view(self):
        self.update_lambda()
        text = 'participant view Dinis Cruz'
        self.result = self.aws_lambda.invoke({'event': {'type': 'message', 'text': text, "channel": "DJ8UA0RFT"}})