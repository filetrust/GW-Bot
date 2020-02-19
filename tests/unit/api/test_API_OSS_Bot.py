from osbot_aws.Dependencies import upload_dependency
from osbot_aws.apis.Lambda import Lambda

from gw_bot.api.API_OSS_Bot import API_OSS_Bot
from gw_bot.helpers import Lambda_Helpers
from gw_bot.helpers.Test_Helper import Test_Helper


class test_API_OSS_Bot(Test_Helper):

    def setUp(self):
        super().setUp()
        self.api    = API_OSS_Bot()
        self.result = None

    def test_resolve_bot_token(self):
        assert type(self.api.resolve_bot_token()) is str

    def test_send_message(self):
        self.response = self.api.send_message('DRE51D4EM', 'test message',[])

    def test_handle_file_drop(self):
        slack_event = {  "type": "file_created",
                         "file": {"id": "FSWQ0UYGP" },
                         "file_id": "FSWQ0UYGP",
                          "user_id": "URS8QH4UF",
                          "event_ts": "1579473069.000200"}
        self.result = self.api.handle_file_drop(slack_event)
    # channel = 'DJ8UA0RFT'
    # user = 'UAULZ1T98'


    def test_via_lambda_handle_file_drop(self):
        super().lambda_package('gw_bot.lambdas.gw_bot').update_code()

        slack_event = {"type": "file_created",
                       "file": {"id": "FSWQ0UYGP"},
                       "file_id": "FSWQ0UYGP",
                       "user_id": "URS8QH4UF",
                       "event_ts": "1579473069.000200"}
        paylaod = {'event': slack_event}
        self.result = Lambda('gw_bot.lambdas.gw_bot').invoke(paylaod)


    def test_upload_dependency(self):
        upload_dependency("slack")
