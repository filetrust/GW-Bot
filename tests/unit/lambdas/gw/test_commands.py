from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.gw.commands import run


class test_gw_engine(Test_Helper):
    def setUp(self):
        super().setUp()
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw.commands')
        self.params     = {'params': ['api_keys'], 'data': {'client_msg_id': '5ad9ca83-142f-4ba1-9c57-7179fd164859', 'type': 'message', 'text': 'gw api_keys', 'user': 'UR9UENEAW', 'ts': '1581216116.020000', 'team': 'TRQU3V52S', 'blocks': [{'type': 'rich_text', 'block_id': 'BLw', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'gw api_keys'}]}]}], 'channel': 'DRE51D4EM', 'event_ts': '1581216116.020000', 'channel_type': 'im'}}

    def test_update_lambda(self):
        self.aws_lambda.update_code()

    def test_invoke_directy(self):
        self.result = run(self.params, None)

    def test_invoke_via_lambda(self):
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke(self.params)