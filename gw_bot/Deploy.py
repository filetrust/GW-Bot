from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Lambda_Package import Lambda_Package
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files

from gw_bot.setup.OSS_Setup import OSS_Setup


class Deploy:

    def __init__(self):
        self.oss_setup     = OSS_Setup()

    def setup(self):
        self.oss_setup.setup_test_environment()
        return self

    def get_package(self, lambda_name):
        package = Lambda_Package(lambda_name)
        package._lambda.set_s3_bucket(self.oss_setup.s3_bucket_lambdas) \
                       .set_s3_key('lambdas/{0}.zip'.format(lambda_name)) \
                       .set_role(self.oss_setup.role_lambdas)

        return package

    def deploy_lambda__gw_bot(self, lambda_name='gw_bot.lambdas.gw_bot'):
        return self.get_package(lambda_name).update_code()

    def deploy_lambda__git_lambda(self):
        return self.get_package('gw_bot.lambdas.git_lambda').update_code()

    def deploy_lambda__browser(self, lambda_name='osbot_browser.lambdas.lambda_browser'):
        package = self.get_package(lambda_name)
        source_folder = Files.path_combine(__file__,'../../modules/OSBot-Browser/osbot_browser')
        package.add_folder(source_folder)
        gw_bot_folder = Files.path_combine(__file__, '../../gw_bot')         # this is needed because of some of the helpers (which will need to be refactored into a separate module)
        package.add_folder(gw_bot_folder)
        package.add_module('osbot_aws')
        package.add_pbx_gs_python_utils()
        package.update()
        return package

    def deploy_lambda__jira(self, lambda_name=None):
        if lambda_name:
            package = self.get_package(lambda_name)
            source_folder = Files.path_combine(__file__,'../../modules/OSBot-jira/osbot_jira')
            package.add_folder(source_folder)
            gw_bot_folder = Files.path_combine(__file__,'../../gw_bot')  # this is needed because of some of the helpers (which will need to be refactored into a separate module)
            package.add_folder(gw_bot_folder)
            package.add_module('osbot_aws')
            package.add_pbx_gs_python_utils()
            package.update()
            return package

    def deploy_lambda__jupyter(self, lambda_name=None, include_osbot_browser=False):
        if lambda_name:
            package = self.get_package(lambda_name)
            if include_osbot_browser:
                source_folder = Files.path_combine(__file__, '../../modules/OSBot-Browser/osbot_browser')
                package.add_folder(source_folder)
            source_folder = Files.path_combine(__file__,'../../modules/OSBot-Jupyter/osbot_jupyter')
            package.add_folder(source_folder)
            gw_bot_folder = Files.path_combine(__file__,'../../gw_bot')  # this is needed because of some of the helpers (which will need to be refactored into a separate module)
            package.add_folder(gw_bot_folder)
            package.add_module('osbot_aws')
            package.add_pbx_gs_python_utils()
            package.update()
            return package

    def deploy_lambda__slack_message(self):
        package = self.get_package('pbx_gs_python_utils_lambdas_utils_slack_message')
        package._lambda.handler = 'gw_bot.lambdas.slack_message.run'
        package.add_module('gw_bot')
        package.add_module('osbot_aws')
        package.add_pbx_gs_python_utils()
        package.delete()
        package.update()

    def deploy_lambda_log_to_elk(self):
        lambda_name = 'gw_bot_utils_log_to_elk'
        package = self.get_package(lambda_name)
        package._lambda.handler = 'gw_bot.lambdas.log_to_elk.run'
        package.add_module('gw_bot')
        package.add_module('osbot_aws')
        package.add_pbx_gs_python_utils()
        package.update()
        return package

    def deploy_lambda_png_to_slack(self):
        lambda_name = 'utils_png_to_slack'
        package = self.get_package(lambda_name)
        package._lambda.handler = 'gw_bot.lambdas.png_to_slack.run'
        package.add_module('osbot_aws')
        package.add_module('gw_bot')
        package.add_pbx_gs_python_utils()
        package.update()
        return package

    def deploy_lambda_puml_to_slack(self):
        lambda_name = 'utils_puml_to_slack'
        package = self.get_package(lambda_name)
        package._lambda.handler = 'gw_bot.lambdas.puml_to_slack.run'
        package.add_module('osbot_aws')
        package.add_module('gw_bot')
        package.add_pbx_gs_python_utils()
        package.update()
        return package

    def deploy_lambda_puml_to_png(self):
        lambda_name = 'utils_puml_to_png'
        package = self.get_package(lambda_name)
        package._lambda.handler = 'gw_bot.lambdas.puml_to_png.run'
        package.add_module('osbot_aws')
        package.add_module('gw_bot')
        package.add_pbx_gs_python_utils()
        package.update()
        return package


    def deploy_lambda__slack_web(self):
        package = self.get_package('osbot_browser.lambdas.slack_web')
        source_folder = Files.path_combine(__file__,'../../modules/OSBot-Browser/osbot_browser')
        package.add_folder(source_folder)
        package.add_module('osbot_aws')
        package.add_module('gw_bot')
        package.add_pbx_gs_python_utils()
        package.update()
        return package


