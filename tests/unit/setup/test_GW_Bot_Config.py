from gw_bot.setup.GWBot_Config import GW_Bot_Config
from osbot_utils.testing.Unit_Test import Unit_Test
from osbot_utils.utils.Files import file_exists


class test_GW_Bot_config(Unit_Test):

    def setUp(self):
        super().setUp()
        self.gw_bot_config = GW_Bot_Config()

    def test__init__(self):
        assert file_exists(self.gw_bot_config.config_file)

    def test_config(self):
        self.result = self.gw_bot_config.config()

    def test_slack_allowed_users(self):
        self.result = self.gw_bot_config.slack_allowed_users()

    def test_version(self):
        assert self.gw_bot_config.version() == GW_Bot_Config().config().get('version')