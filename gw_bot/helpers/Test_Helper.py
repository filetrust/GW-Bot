import base64
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.setup.OSS_Setup import OSS_Setup


class Test_Helper(TestCase):


    def setUp(self) -> OSS_Setup:
        return self.oss_setup()

    def oss_setup(self,profile_name = None, account_id=None, region=None) -> OSS_Setup:
        self.result   = None
        self.png_data = None
        self.png_file = '/tmp/lambda_png_file.png'
        return OSS_Setup(profile_name=profile_name,account_id=account_id,region=region).setup_test_environment()

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)
        if self.png_data is not None:
            if type(self.png_data) is not str:
                Dev.pprint(f'Png data was not a string: {self.png_data}')
            else:
                try:
                    with open(self.png_file, "wb") as fh:
                        fh.write(base64.decodebytes(self.png_data.encode()))
                    Dev.pprint(f'Png data with size {len(self.png_data)} saved to {self.png_file}')
                except Exception as error:
                    Dev.pprint(f'png save error: {error}')
                    Dev.pprint(self.png_data)

    def lambda_package(self, lambda_name, profile_name = None, account_id=None, region=None):
        return self.oss_setup(profile_name=profile_name,account_id=account_id,region=region).lambda_package(lambda_name)

    @staticmethod
    def print(result):
        if result is not None:
            Dev.pprint(result)

    @staticmethod
    def save_png(png_data, target_file):
        if png_data is not None:
            with open(target_file, "wb") as fh:
                fh.write(base64.decodebytes(png_data.encode()))
