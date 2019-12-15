from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.setup.OSS_Setup import OSS_Setup


class test_OSS_Setup(Test_Helper):
    def setUp(self):
        self.oss_setup = OSS_Setup()
        super().setUp()


    def test__init__(self):
        assert self.oss_setup.profile_name == 'gw-bot'

    def test_lambda_package(self):
        self.lambda_package = self.oss_setup.lambda_package('an-lambda-name')

        assert self.lambda_package.lambda_name   == 'an-lambda-name'
        assert self.lambda_package.tmp_s3_bucket == self.oss_setup.s3_bucket_lambdas
        assert self.lambda_package.tmp_s3_key    == 'lambdas/an-lambda-name.zip'

        #self.result = self.lambda_package.tmp_s3_key


    def test_set_up_buckets(self):
        self.result =self.oss_setup.set_up_buckets()
        assert self.oss_setup.s3_bucket_lambdas in self.oss_setup.s3.buckets()


