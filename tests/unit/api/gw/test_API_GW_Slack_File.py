from gw_bot.api.gw.API_GW_Slack_File import API_GW_Slack_File
from gw_bot.helpers.Test_Helper import Test_Helper


class test_API_GW_Slack_File(Test_Helper):

    def setUp(self):
        super().setUp()
        self.api = API_GW_Slack_File()
        self.slack_event = { "type"    : "file_created",
                            "file"    : {"id": "FSWQ0UYGP"},
                            "file_id" : "FSWQ0UYGP",
                            "user_id" : "URS8QH4UF",
                            "event_ts": "1579473069.000200"}

        #self.slack_event['file_id'] = 'FSHGD2QR1'

    def test_file_info_form_slack(self):
        self.result = self.api.file_info_form_slack(self.slack_event)

    def test_download_file(self):
        file_info = self.api.file_info_form_slack(self.slack_event)
        self.result = self.api.download_file(file_info)

    def test_scan_file(self):
        self.result = self.api.gw_scan_file('/tmp/3uni12ba/gcon-sessions.pdf')