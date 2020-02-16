def run(event, context):
    from gw_bot.api.Slack_Commands_Helper import Slack_Commands_Helper
    from gw_bot.api.commands.aws.AWS_Commands import AWS_Commands
    params  = event.get('params',{})
    data    = event.get('data'  ,{})
    channel = data.get('channel')


    result,_ = Slack_Commands_Helper(AWS_Commands).invoke(channel=channel, params=params)
    if channel is None:
        return result
    return result