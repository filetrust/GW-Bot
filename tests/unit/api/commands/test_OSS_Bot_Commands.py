from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from gw_bot.api.commands.OSS_Bot_Commands import OSS_Bot_Commands
from gw_bot.helpers.Test_Helper import Test_Helper


class test_OSS_Bot_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_browser(self):
        self.result = OSS_Bot_Commands.browser()

    def test_hello(self):
        assert OSS_Bot_Commands.hello() == ('Hello <@None>, how can I help you?', [])

    def test_gw(self):
        self.result = OSS_Bot_Commands.gw()

    def test_jira(self):
        self.result = OSS_Bot_Commands.jira({}, [])


    def test_help(self):
        assert OSS_Bot_Commands.help()[0] ==  '*Here are the commands available*'

    def test_site(self):
        self.result = OSS_Bot_Commands.site()

    def test_screenshot(self):
        self.result = OSS_Bot_Commands.screenshot(None, ['abc'])

    def test_participant(self):
        self.result = OSS_Bot_Commands.participant({'channel': 'CJ91NQX17'},['ping'])

    def test_version(self):
        assert OSS_Bot_Commands.version()[0] == OSS_Bot_Commands.gsbot_version



    # deploy helpers

    def test_deploy_lambda__gw_bot(self):
        Deploy().setup().deploy_lambda__gw_bot()


