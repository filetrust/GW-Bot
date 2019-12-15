from osbot_aws.apis.Lambda import Lambda

from gw_bot.api.API_OSS_Slack import API_OSS_Slack

class Dev_Commands:

    @staticmethod
    def ping(*event):
        return 'pong : {0}'.format(event)

    @staticmethod
    def my_name(slack_id, channel,params):
        return "your real name is {0}".format(API_OSS_Slack().slack_id_to_slack_full_name(slack_id))

    @staticmethod
    def resolve(slack_id, channel, params):
        slack_id= "".join(params).replace('<@','').replace('>','')
        return API_OSS_Slack().slack_id_to_slack_full_name(slack_id)


    @staticmethod
    def git_diff(team_id=None, channel=None, params=None):
        aws_lambda = Lambda('gw_bot.lambdas.git_lambda')
        payload = {'action' : 'git_dff' ,
                   'channel': channel            ,
                   'commit' : False              }
        aws_lambda.invoke_async(payload)

    @staticmethod
    def git_status(team_id=None, channel=None, params=None):
        aws_lambda = Lambda('gw_bot.lambdas.git_lambda')
        payload = {'action': 'git_status',
                   'channel': channel,
                   'commit': False}
        aws_lambda.invoke_async(payload)

    @staticmethod
    def git_pull(team_id=None, channel=None, params=None):
        aws_lambda = Lambda('gw_bot.lambdas.git_lambda')
        payload = {'action': 'git_pull',
                   'channel': channel,
                   'commit': False}
        aws_lambda.invoke_async(payload)

    @staticmethod
    def git_reset(team_id=None, channel=None, params=None):
        aws_lambda = Lambda('gw_bot.lambdas.git_lambda')
        payload = {'action': 'git_reset',
                   'channel': channel,
                   'commit': False}
        aws_lambda.invoke_async(payload)
