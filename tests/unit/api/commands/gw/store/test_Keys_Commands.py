from gw_bot.api.commands.gw.store.Keys_Commands import Keys_Commands
from gw_bot.helpers.Test_Helper import Test_Helper


class test_Keys_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.keys_commands = Keys_Commands()

    def test_create__delete(self):
        #self.keys_commands.create(None,None,['new key name'])
        self.result = self.keys_commands.delete(None,None,['new key name'])

    def test_list(self):
        self.result = self.keys_commands.list(None,None,[])

    def test_usage_plans(self):
        self.result = self.keys_commands.usage_plans(None,None,[])

    def test_usage_plans_keys(self):
        self.result = self.keys_commands.usage_plan_keys(None,None,['d0fhi9'])

    def test_update_lambda(self):
        super().lambda_package('gw_bot.lambdas.gw.store').update_code()