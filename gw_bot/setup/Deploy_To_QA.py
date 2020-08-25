from osbot_aws.Globals import Globals
from osbot_aws.apis.IAM import IAM
from osbot_aws.apis.S3 import S3


class Deploy_To_QA:

    def __init__(self):
        self.account_id = '195337790717'
        self.profile_id  = f'{self.account_id}_AdministratorAccess'
        self.bucket_name = f'{self.account_id}_owbot_lambdas'
        self.deploy_user = f'owbot_deploy_user'

    def setup_aws(self):
        Globals.aws_session_profile_name = self.profile_id

        #return S3().buckets()
        #return IAM().users_by_username()


    def setup_deploy_user(self):
        iam = IAM(user_name=self.deploy_user)
        iam.user_create()

        assert iam.user_exists()
