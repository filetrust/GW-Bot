from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from gw_bot.api.commands.Participant_Commands import Participant_Commands
from gw_bot.api.commands.Schedule_Commands import Schedule_Commands
from gw_bot.helpers.Test_Helper import Test_Helper


class test_Schedule_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_today(self):
        Schedule_Commands.today(None,'DJ8UA0RFT',[])
