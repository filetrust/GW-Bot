from gw_bot.api.gw.API_Glasswall import API_Glasswall
from osbot_aws.helpers.Test_Helper import Test_Helper

class test_gw_engine(Test_Helper):
    def setUp(self):
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw.gw_engine')

    def test_update_lambda(self):
        self.aws_lambda.update_code()

    def test__invoke_via_lambda(self):
        self.test_update_lambda()

        target_file = '/tmp/Macros.xls'
        #target_file = '/Users/diniscruz//Downloads/Macros.xls'

        (file_name, base64_data) = API_Glasswall().get_file_base_64(target_file)
        payload = {'file_contents' : base64_data , 'file_name': file_name }

        self.result = self.aws_lambda.invoke(payload)
