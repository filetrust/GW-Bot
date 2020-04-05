from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.dot_to_svg  import run
from osbot_aws.apis.Lambda      import Lambda
from osbot_utils.utils.Files    import file_create


class Test_Lambda_dot_to_png(Test_Helper):

    def setUp(self):
        super().setUp()
        self.lambda_name = 'gw_bot.lambdas.dot_to_svg'
        self.dot_to_png = Lambda(self.lambda_name)
        self.test_dot = """digraph G {
                              a1 -> b3;
                              b2 -> a3;
                              a3 -> a0;
                              a3 -> end;
                              b3 -> endAAA;                                                                                       
                              #{ rank=source ; b2 }
                           }"""

    def test_deploy_lambda(self):
        self.result  = Deploy().deploy_lambda__gw_bot(self.lambda_name)

    def test_invoke_directly(self):
        self.result = run({})

    # images = {'/tmp/ACCESS.png'  : Jira_Icons().github_url('access'),
    #           '/tmp/RISK.png'    : Jira_Icons().github_url('risk') ,
    #           '/tmp/CLIENT.png'  : Jira_Icons().github_url('client') }

    def test_lambda_invoke(self):
        self.test_deploy_lambda()
        params = {'dot': self.test_dot, 'layout_engine':'dot' }
        self.result = self.dot_to_png.invoke(params)

        if self.result.get('svg'):
            file_create('/tmp/dot_image.svg',self.result.get('svg'))
