from osbot_utils.utils.Dev import Dev

from gw_bot.api.commands.Schedule_Commands import Schedule_Commands
from osbot_aws.helpers.Test_Helper import Test_Helper


class test_Schedule_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_today(self):
        Schedule_Commands.today(None,'DJ8UA0RFT',[])
