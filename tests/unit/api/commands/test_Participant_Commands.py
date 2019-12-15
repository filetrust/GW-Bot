from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from gw_bot.api.commands.Participant_Commands import Participant_Commands
from gw_bot.helpers.Test_Helper import Test_Helper


class test_Participant_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_info(self):
        self.result = Participant_Commands.info(None,'DJ8UA0RFT')

    def test_view(self):
        self.result = Participant_Commands.view(None,'DJ8UA0RFT',['OSS Bot'])

    def test_edit(self):
        self.result = Participant_Commands.edit(None,'DJ8UA0RFT',['OSS Bot,test_field,abc'])

    # deploy helpers

    def test_deploy_lambda__oss_bot(self):
        Deploy().setup().deploy_lambda__oss_bot()


    def test_deploy_lambda__git_lambda(self):
        return Deploy().deploy_lambda__git_lambda()