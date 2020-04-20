from gw_bot.Deploy import Deploy
from gw_bot.lambdas.dev.hello_world import run
#from osbot_aws.apis.Lambdas import Lambdas
from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.test_helpers.Temp_Aws_Roles import Temp_Aws_Roles
from gw_bot.helpers.Test_Helper import Test_Helper


class test_run_command(Test_Helper):
    def setUp(self):
        super().setUp()
        self.lambda_name = 'gw_bot.lambdas.dev.hello_world'
        self.aws_lambda   = Lambda(self.lambda_name)
        #self.aws_lambda.add_module('gw_bot')

    def test_update_lambda(self):
        Deploy().deploy_lambda__gw_bot(self.lambda_name)

    # this test needs to be executed once (since it will create the role used for these executions)
    def test_create_aws_role(self):
        aws_role_lambda = Temp_Aws_Roles().create__for_lambda_invocation()
        assert aws_role_lambda == 'arn:aws:iam::311800962295:role/temp_role_for_lambda_invocation'
        #self.result = aws_role_lambda

    # this test will check that that everything required to run the lambda has been correctly setup
    def test_create(self):
        self.aws_lambda._lambda.upload()
        self.aws_lambda.create()
        assert 'gw_bot_lambdas_dev_hello_world'              in list(set(Lambda().list()))
        assert 'lambdas/gw_bot.lambdas.dev.hello_world.zip'  in self.aws_lambda._lambda.s3().find_files('gw-bot-lambdas','lambdas')

    def test_invoke_directly(self):
        self.result = run({},{})

    def test_just_update(self):
        self.aws_lambda.update()

    # test the invocation
    def test_update_and_invoke(self):
        self.test_update_lambda()
        assert self.aws_lambda.invoke({'name':'abc'}) == {'body': 'Hello abc (from lambda)',
                                                         'headers': {},
                                                         'isBase64Encoded': False,
                                                         'statusCode': 200}

    # test the invocation
    def test_just_invoke(self):
        #self.test_update_lambda()
        self.result = self.aws_lambda.invoke({'name': 'abc'})


        #assert self.aws_lambda.invoke({'name': 'abc'}) == 'Hello abc (from lambda)'