from osbot_aws.apis.Lambda import Lambda
from osbot_utils.utils import Misc
from osbot_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from osbot_aws.helpers.Test_Helper import Test_Helper


class test_git_lambda(Test_Helper):
    def setUp(self):
        self.osbot_setup = super().setUp()
        # self.aws_lambda = Lambda_Package('gw_bot.lambdas.git_lambda')
        # self.aws_lambda._lambda.set_s3_bucket(self.osbot_setup.s3_bucket_lambdas)         \
        #                        .set_role     (self.osbot_setup.role_lambdas)
        self.aws_lambda = Lambda('gw_bot.lambdas.git_lambda')
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_update_lambda(self):
        return Deploy().deploy_lambda__git_lambda()

    def test_invoke_files(self):
        self.test_update_lambda()
        self.aws_lambda.invoke({'command': 'clone'})
        #self.aws_lambda.invoke({'command': 'clone'})
        payload = {'command': '__files'}
        self.result = self.aws_lambda.invoke(payload)

    def test_git_status(self):
        self.test_update_lambda()
        payload = { 'action': 'git_status',
                    'commit': False       }
        self.result = self.aws_lambda.invoke(payload)

    def test_git_diff(self):
        self.test_update_lambda()
        payload = { 'action': 'git_diff',
                    'commit': False       }
        self.result = self.aws_lambda.invoke(payload)

    def test_participant_info(self):
        self.test_update_lambda()
        payload = { 'action': 'participant_info',
                    'name'  : 'OSS Bot'         ,
                    'commit': False}
        self.result = self.aws_lambda.invoke(payload)

        #assert self.aws_lambda.invoke(payload) == {'status': 'ok'}

    def test_participant_url(self):
        self.test_update_lambda()
        payload = { 'action': 'participant_url',
                    'name'  : 'OSS Bot'         ,
                    'commit': False}
        self.result = self.aws_lambda.invoke(payload)

    def test_participant_edit_field(self):

        payload = { 'action': 'participant_edit_field',
                    'name'  : 'OSS Bot'         ,
                    'field' : 'test_field'      ,
                    'value' : Misc.random_string_and_numbers() }
        assert self.aws_lambda.invoke(payload) == {'status': 'ok'}


    def test_participant_append_to_field(self):
        payload = {'action': 'participant_append_to_field',
                   'name': 'OSS Bot',
                   'field': 'test_field',
                   'value': Misc.random_string_and_numbers()}
        assert self.aws_lambda.invoke(payload) == {'status': 'ok'}

        payload = {'action': 'participant_append_to_field',
                   'name': 'OSS Bot',
                   'field': 'sessions',
                   'value': Misc.random_string_and_numbers()}

        assert self.aws_lambda.invoke(payload) == {'status': 'ok'}

    def test_participant_remove_from_field_str(self):
        payload = {'action': 'participant_edit_field'            ,
                   'name'  : 'OSS Bot'                           ,
                   'field' : 'test_field'                        ,
                   'value' : 'an value - 123'                    }
        assert self.aws_lambda.invoke(payload) == {'status': 'ok'}

        payload = {'action': 'participant_remove_from_field',
                   'name'  : 'OSS Bot'                      ,
                   'field' : 'test_field'                   ,
                   'value' : ' - 123'                       }

        assert self.aws_lambda.invoke(payload) == {'status': 'ok'}

    def test_participant_remove_from_field_list(self):
        value = 'temp_session'
        payload = {'action': 'participant_append_to_field'            ,
                   'name'  : 'OSS Bot'                           ,
                   'field' : 'sessions'                          ,
                   'value' : value                               }
        assert self.aws_lambda.invoke(payload) == {'status': 'ok'}

        payload = {'action': 'participant_remove_from_field'     ,
                   'name'  : 'OSS Bot'                           ,
                   'field' : 'sessions'                          ,
                   'value' :  value                              }

        #self.result = self.aws_lambda.invoke(payload)
        assert self.aws_lambda.invoke(payload) == {'status': 'ok'}