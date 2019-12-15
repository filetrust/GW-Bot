from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.setup.OSS_Setup import OSS_Setup


class Test_Helper(TestCase):


    def setUp(self) -> OSS_Setup:
        self.result = None
        return OSS_Setup().setup_test_environment()

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def lambda_package(self, lambda_name):
        self.result = None
        return OSS_Setup().setup_test_environment().lambda_package(lambda_name)