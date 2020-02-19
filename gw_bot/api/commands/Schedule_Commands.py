from gw_bot.helpers.Lambda_Helpers import slack_message

from gw_bot.api.API_OSS_Slack import API_OSS_Slack
from gw_bot.api.commands.Participant_Commands import Participant_Commands
from gw_bot.api.commands.Participant_Commands import send_screenshot_to_slack


class Schedule_Commands:

    @staticmethod
    def today(*event):
        channel = event[1]
        slack_message(":mag_right: Ok, fetching the latest version of today's schedule :mag:", [], channel)
        params = ['oss_today']
        slack_event = {'channel': event[1]}
        from osbot_aws.apis.Lambda import Lambda
        Lambda('osbot_browser.lambdas.lambda_browser').invoke_async({'params': params, 'data': slack_event}), []
        #send_screenshot_to_slack('schedule/day/mon', event[1], [1200])

    @staticmethod
    def tuesday(*event):
        send_screenshot_to_slack('schedule/day/tue', event[1], [1200])

    @staticmethod
    def wednesday(*event):
        send_screenshot_to_slack('schedule/day/wed', event[1], [1200])

    @staticmethod
    def mine(slack_id, channel,params):
        slack_message(":mag_right: Ok, fetching scheadule for <@{0}>".format(slack_id), [], channel)
        name = API_OSS_Slack().slack_id_to_slack_full_name(slack_id)

        text = 'participant view {0}'.format(name)
        from osbot_aws.apis.Lambda import Lambda
        aws_lambda = Lambda('gw_bot.lambdas.gw_bot')
        aws_lambda.invoke_async({'event': {'type': 'message', 'text': text, "channel": channel}})
        # Participant_Commands.view(slack_id, channel, [name])

    @staticmethod
    def of_participant(slack_id, channel, params):
        slack_id= "".join(params).replace('<@','').replace('>','')
        name = API_OSS_Slack().slack_id_to_slack_full_name(slack_id)


