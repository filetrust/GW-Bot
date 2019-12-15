from gw_bot.api.API_OSS_Bot import API_OSS_Bot
from gw_bot.helpers.Test_Helper import Test_Helper


class test_API_OSS_Bot(Test_Helper):

    def setUp(self):
        super().setUp()
        self.api = API_OSS_Bot()

    def test_resolve_bot_token(self):
        assert type(self.api.resolve_bot_token()) is str

    def test_send_message(self):
        self.response = self.api.send_message('DJ8UA0RFT', 'test message',[])
    # channel = 'DJ8UA0RFT'
    # user = 'UAULZ1T98'

