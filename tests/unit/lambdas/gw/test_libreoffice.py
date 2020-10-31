from gw_bot.api.gw.API_Glasswall import API_Glasswall
from osbot_aws.helpers.Test_Helper import Test_Helper


class test_gw_report(Test_Helper):

    def setUp(self):
        super().setUp()
        self.aws_lambda = super().lambda_package('gw_bot.lambdas.gw.libreoffice')

    def payload(self):
        target_file = '/tmp/test_file.png'
        (file_name, base64_data) = API_Glasswall().get_file_base_64(target_file)
        return {'file_contents': base64_data, 'file_name': file_name}

    def test_update_lambda(self):
        self.aws_lambda.update_code()

    def test__update_and_invoke(self):
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke(self.payload())

    def test__invoke(self):
        self.result = self.aws_lambda.invoke(self.payload())
