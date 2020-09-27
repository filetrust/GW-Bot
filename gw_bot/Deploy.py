from osbot_aws.helpers.Lambda_Package import Lambda_Package
from gw_bot.setup.OSBot_Setup         import OSBot_Setup
from osbot_utils.utils.Files          import path_combine

class Deploy:

    def __init__(self):
        self.osbot_setup     = OSBot_Setup()

    def setup(self):
        #self.osbot_setup.setup_test_environment()
        return self

    def get_package(self, lambda_name):
        package = Lambda_Package(lambda_name)
        package.aws_lambda.set_s3_bucket(self.osbot_setup.s3_bucket_lambdas) \
                          .set_role(self.osbot_setup.lambda_role_arn)
                          #.set_s3_key('lambdas/{0}.zip'.format(lambda_name)) \

        return package

    def deploy_lambda__gw_bot(self, lambda_name='gw_bot.lambdas.gw_bot'):
        package = self.get_package(lambda_name)
        package.add_folder(path_combine(__file__, '../../gw_bot'))
        package.add_module('osbot_aws')
        package.add_osbot_utils()
        return package.update()


    # def deploy_lambda__git_lambda(self):
    #     return self.get_package('gw_bot.lambdas.git_lambda').update_code()

    def deploy_lambda__browser(self, lambda_name='osbot_browser.lambdas.lambda_browser'):
        package = self.get_package(lambda_name)
        source_folder = path_combine(__file__,'../../modules/OSBot-browser/osbot_browser')
        package.add_folder(source_folder)
        gw_bot_folder = path_combine(__file__, '../../gw_bot')         # this is needed because of some of the helpers (which will need to be refactored into a separate module)
        package.add_folder(gw_bot_folder)
        package.add_module('osbot_aws')
        package.add_osbot_utils()
        package.update()
        return package

    def deploy_lambda__browser_dev(self, lambda_name):
        package = self.get_package(lambda_name)
        source_folder = path_combine(__file__, '../../modules/OSBot-browser/osbot_browser')
        package.add_folder(source_folder, ignore = 'web_root')
        package.add_module('osbot_aws')
        package.add_module('osbot_utils')
        package.update()
        return package

    def deploy_lambda__jira(self, lambda_name=None):
        if lambda_name:
            package = self.get_package(lambda_name)
            source_folder = path_combine(__file__,'../../modules/OSBot-jira/osbot_jira')
            package.add_folder(source_folder)
            gw_bot_folder = path_combine(__file__,'../../gw_bot')  # this is needed because of some of the helpers (which will need to be refactored into a separate module)
            package.add_folder(gw_bot_folder)
            package.add_module('osbot_aws')
            #package.add_module('pbx_gs_python_utils')       # todo: remove dependencies (or currently functions like 'osbot_jira.lambdas.jira' will fail in lambda)
            package.add_osbot_utils()
            package.update()
            return package

    def deploy_lambda__jupyter(self, lambda_name=None):
        if lambda_name:
            package = self.get_package(lambda_name)
            source_folder = path_combine(__file__,'../../modules/OSBot-Jupyter/osbot_jupyter')
            package.add_folder(source_folder)
            gw_bot_folder = path_combine(__file__,'../../gw_bot')  # this is needed because of some of the helpers (which will need to be refactored into a separate module)
            package.add_folder(gw_bot_folder)
            package.add_module('osbot_aws')
            #package.add_module('pbx_gs_python_utils')  # todo: remove dependencies (or currently functions like 'osbot_jira.lambdas.jira' will fail in lambda)
            package.add_osbot_utils()
            package.update()
            return package

    def deploy_lambda__jupyter_web(self, lambda_name=None):     # for the cases where osbot_browser is needed
        if lambda_name:
            package = self.get_package(lambda_name)
            source_folder = path_combine(__file__, '../../modules/OSBot-browser/osbot_browser')
            package.add_folder(source_folder)
            source_folder = path_combine(__file__,'../../modules/OSBot-Jupyter/osbot_jupyter')
            package.add_folder(source_folder)
            gw_bot_folder = path_combine(__file__,'../../gw_bot')  # this is needed because of some of the helpers (which will need to be refactored into a separate module)
            package.add_folder(gw_bot_folder)
            package.add_module('osbot_aws')
            package.add_osbot_utils()
            package.update()
            return package



    # def deploy_lambda__slack_message(self):
    #     package = self.get_package('pbx_gs_python_utils_lambdas_utils_slack_message')
    #     package.aws_lambda.handler = 'gw_bot.lambdas.slack_message.run'
    #     package.add_module('gw_bot')
    #     package.add_module('osbot_aws')
    #     package.add_pbx_gs_python_utils()
    #     package.delete()
    #     package.update()
    #
    # def deploy_lambda_log_to_elk(self):
    #     lambda_name = 'gw_bot_utils_log_to_elk'
    #     package = self.get_package(lambda_name)
    #     package.aws_lambda.handler = 'gw_bot.lambdas.log_to_elk.run'
    #     package.add_module('gw_bot')
    #     package.add_module('osbot_aws')
    #     package.add_pbx_gs_python_utils()
    #     package.update()
    #     return package
    #
    # def deploy_lambda_png_to_slack(self):
    #     lambda_name = 'utils_png_to_slack'
    #     package = self.get_package(lambda_name)
    #     package.aws_lambda.handler = 'gw_bot.lambdas.png_to_slack.run'
    #     package.add_module('osbot_aws')
    #     package.add_module('gw_bot')
    #     package.add_pbx_gs_python_utils()
    #     package.update()
    #     return package
    #
    # def deploy_lambda_puml_to_slack(self):
    #     lambda_name = 'utils_puml_to_slack'
    #     package = self.get_package(lambda_name)
    #     package.aws_lambda.handler = 'gw_bot.lambdas.puml_to_slack.run'
    #     package.add_module('osbot_aws')
    #     package.add_module('gw_bot')
    #     package.add_pbx_gs_python_utils()
    #     package.update()
    #     return package
    #
    # def deploy_lambda_puml_to_png(self):
    #     lambda_name = 'utils_puml_to_png'
    #     package = self.get_package(lambda_name)
    #     package.aws_lambda.handler = 'gw_bot.lambdas.puml_to_png.run'
    #     package.add_module('osbot_aws')
    #     package.add_module('gw_bot')
    #     package.add_pbx_gs_python_utils()
    #     package.update()
    #     return package


    # def deploy_lambda__slack_web(self):
    #     package = self.get_package('osbot_browser.lambdas.slack_web')
    #     source_folder = path_combine(__file__,'../../modules/OSBot-browser/osbot_browser')
    #     package.add_folder(source_folder)
    #     package.add_module('osbot_aws')
    #     package.add_module('gw_bot')
    #     package.add_pbx_gs_python_utils()
    #     package.update()
    #     return package


