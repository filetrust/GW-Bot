import base64

from osbot_utils.utils.Dev import Dev

from osbot_browser.lambdas.lambda_browser import run
from osbot_aws.apis.Lambda import Lambda

from gw_bot.Deploy import Deploy
from osbot_aws.helpers.Test_Helper import Test_Helper


class test_run_command(Test_Helper):
    def setUp(self):
        self.osbot_setup  = super().setUp()
        self.aws_lambda = Lambda('osbot_browser.lambdas.lambda_browser')
        self.result     = None
        self.png_data   = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)
        if self.png_data:
            png_file = '/tmp/lambda_png_file.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))

    def test__invoke__directly(self):
        self.result = run({},{})

    def test__invoke__no_params(self):
        assert self.aws_lambda.invoke() == '*Here are the `Browser_Commands` commands available:*'

    def test__invoke__version(self):
        payload = { "params" :["version"]}
        self.result = self.aws_lambda.invoke(payload)

    def test__update_lambda(self):
        Deploy().deploy_lambda__browser()

    def test__invoke__screenshot(self):
        payload = {"params": ["screenshot", "https://www.google.com/images", "1200"],
                   'data': {'channel': 'DRE51D4EM'}}
        self.result = self.aws_lambda.invoke(payload)
        #self.png_data = self.aws_lambda.invoke(payload)

    def test__invoke__screenshot__no_channel(self):
        payload = {"params": ["screenshot", "https://www.google.com/images"]}
        self.result = self.aws_lambda.invoke(payload)

    # Bugs

    def test_bug_ResourceNotFoundException(self):
        url = 'https://wwww.google.com'         # bad url (extra w in path)
        payload = {"params": ['screenshot', url]}
        # invoke directly
        #self.result = run(payload, {})

        # invoke via lambda
        #self.test__update_lambda()
        self.result = Lambda('osbot_browser.lambdas.lambda_browser').invoke(payload) #self.aws_lambda.invoke(payload)






