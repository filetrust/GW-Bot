from osbot_aws.Globals import Globals
from osbot_aws.apis.IAM import IAM
from osbot_aws.apis.S3 import S3
from osbot_aws.helpers.Lambda_Package import Lambda_Package


class OSS_Setup:

    def __init__(self, profile_name = None, account_id=None, region=None):
        self.bot_name          = 'gw_bot'
        self.profile_name      = profile_name or 'gw-bot'
        self.region_name       = region       or 'eu-west-1'
        self.account_id        = account_id   or '311800962295' #glasswalltestframework'
        self.role_lambdas      = "arn:aws:iam::{0}:role/gwbot-lambdas-temp".format(self.account_id)
        self.s3_bucket_lambdas = '{0}-lambdas'.format(self.bot_name).replace('_','-')
        self.s3                = S3()

    def lambda_package(self, lambda_name) -> Lambda_Package:
        lambda_package               = Lambda_Package(lambda_name)
        lambda_package.tmp_s3_bucket = self.s3_bucket_lambdas                       # these four method calls need to be refactored
        lambda_package.tmp_s3_key    = 'lambdas/{0}.zip'.format(lambda_name)
        lambda_package._lambda.set_s3_bucket(lambda_package.tmp_s3_bucket)
        lambda_package._lambda.set_s3_key(lambda_package.tmp_s3_key)
        return lambda_package

    def setup_test_environment(self):
        Globals.aws_session_profile_name = self.profile_name
        Globals.aws_session_region_name  = self.region_name
        return self

    def set_up_buckets(self):
        if self.s3_bucket_lambdas not in self.s3.buckets():
            result = self.s3.bucket_create(self.s3_bucket_lambdas,self.region_name)
            assert result.get('status') == 'ok'
        return self



