from unittest import TestCase

from gw_bot.helpers import Lambda_Helpers
from gw_bot.helpers.Test_Helper import Test_Helper


class test_Lambda_Helpers(Test_Helper):
    def setUp(self):
        super().setUp()

    def test_log_info(self):
        Lambda_Helpers.log_info('test info!!!')

    def test_log_debug(self):
        Lambda_Helpers.log_debug('test debug!!!')

    def test_log_error(self):
        Lambda_Helpers.log_error('test error!!!')
