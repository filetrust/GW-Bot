from gw_bot.setup.Deploy_To_QA import Deploy_To_QA
from osbot_aws.apis.IAM import IAM
from osbot_aws.apis.Session import Session
from osbot_utils.testing.Unit_Test import Unit_Test


class test_Deploy_To_QA(Unit_Test):

    def setUp(self):
        super().setUp()
        self.deploy_to_qa = Deploy_To_QA()

    def test_setup_aws(self):
        self.deploy_to_qa.setup_aws()
        IAM().account_id() == self.deploy_to_qa.account_id

        user_arn = 'arn:aws:sts::195337790717:assumed-role/AWSReservedSSO_AdministratorAccess_4975778b3c1af499/dcruz@glasswallsolutions.com'

        self.result = IAM().iam().get_user(UserName=user_arn)

        #sts = Session().client('sts')
        #role_arn = 'arn:aws:iam::195337790717:role/aws-service-role/sso.amazonaws.com/AWSServiceRoleForSSO'
        #role_session_name = 'test_AWSServiceRoleForSSO'
        #assume_role_object = sts.assume_role(RoleArn=role_arn, RoleSessionName=role_session_name,DurationSeconds=3600)

        #self.result = assume_role_object
        #self.result = IAM().roles(index_by='RoleName').keys()

        #self.credentials = assume_role_object['Credentials']
        #self.result = Session().client('sts').get_caller_identity()

        #client('sts')


    def test_setup_deploy_user(self):
        #self.result = self.deploy_to_qa.setup_deploy_user()
        self.result = 123
        #assume_role_object = sts_connection.assume_role(RoleArn=arn, RoleSessionName=ARN_ROLE_SESSION_NAME,DurationSeconds=3600)

