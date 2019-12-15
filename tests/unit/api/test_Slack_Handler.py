from gw_bot.api.Slack_Handler import Slack_Handler
from gw_bot.helpers.Test_Helper import Test_Helper


class test_Slack_Handler(Test_Helper):

    def setUp(self):
        super().setUp()
        self.slack_handler = Slack_Handler()

    def test_run(self):
        self.result = self.slack_handler.run({'event': {'type':'message','text': 'abc'}})
        self.result = self.slack_handler.run({'event': {'type': 'message', 'text': 'hello abc'}})
        self.result = self.slack_handler.run({'event': {'type': 'message', 'text': 'help'}})

        assert self.slack_handler.run({'challenge': 'abc'}) == 'abc'