from osbot_aws.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.aws.on_s3_event import run


class test_gw_engine(Test_Helper):
    def setUp(self):
        self.aws_lambda = super().lambda_package(lambda_name='gw_bot.lambdas.aws.on_s3_event')
        self.params = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3',
                                    'awsRegion'   : 'eu-west-1', 'eventTime': '2020-02-15T17:34:09.152Z',
                                    'eventName'   : 'ObjectCreated:Put',
                                    'userIdentity': {'principalId': 'AWS:AROAINPZFXXCK5LJPKQMW:regionalDeliverySession'}, 'requestParameters': {'sourceIPAddress': '18.140.58.225'}, 'responseElements': {'x-amz-request-id': '058590F2CD5414B6', 'x-amz-id-2': '42LiLtVUsl/WG5+LrVjZdWaiTr8Od9wAZEaa1FZqt5dTbchXsrsJHXl4gMey83h4Ld93S76is+0WkuC1EfaEfx/86hoNgZYc'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': '7db8de74-0b1f-483e-a56e-5f866844953b', 'bucket': {'name': 'gw-tf-cloud-trails', 'ownerIdentity': {'principalId': 'A2VWG7J36R4Q0A'}, 'arn': 'arn:aws:s3:::gw-tf-cloud-trails'}, 'object': {'key': 'test_trail/AWSLogs/311800962295/CloudTrail/ap-southeast-1/2020/02/15/311800962295_CloudTrail_ap-southeast-1_20200215T1730Z_Ve1ataF6cf7u4KP6.json.gz', 'size': 536, 'eTag': '61afe12a1b781cf7bb41f5db023ac067', 'sequencer': '005E482B9235ACA2B1'}}}]}

    def test_update_lambda(self):
        self.result = self.aws_lambda.update_code()

    def test_invoke_directy(self):
        self.result = run(self.params, None)

    def test_invoke_directy__keys(self):
        self.result = run({}, None)

    def test_invoke_lambda(self):
        self.test_update_lambda()
        self.result = self.aws_lambda.invoke(self.params)
