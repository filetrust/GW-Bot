from gw_bot.helpers.Lambda_Helpers import slack_message
from osbot_aws.apis.Lambda import Lambda
from gw_bot.setup.OSS_Setup import OSS_Setup

class AWS_Commands:

    @staticmethod
    def billing(team_id, channel, params):
        lambda_name = 'osbot_browser.lambdas.aws_web'
        Lambda(lambda_name).invoke({'channel': channel})

    @staticmethod
    def restart_lambdas(team_id, channel, params):
        slack_message(':point_right: restarting Lambda function: `osbot_browser.lambdas.jira_web`' ,[], channel)
        OSS_Setup().lambda_package('osbot_browser.lambdas.jira_web').update_lambda_code()