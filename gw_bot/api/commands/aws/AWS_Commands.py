from osbot_aws.helpers.Lambda_Helpers import slack_message
from osbot_aws.apis.Lambda import Lambda
from gw_bot.setup.OSBot_Setup import OSBot_Setup

class AWS_Commands:

    @staticmethod
    def billing(team_id, channel, params):
        lambda_name = 'osbot_browser.lambdas.aws_web'
        Lambda(lambda_name).invoke({'channel': channel})

    @staticmethod
    def reset_lambdas(team_id, channel, params):
        slack_message(':point_right: restarting Lambda function: `osbot_browser.lambdas.jira_web`' ,[], channel)
        OSBot_Setup().lambda_package('osbot_browser.lambdas.jira_web').reset()