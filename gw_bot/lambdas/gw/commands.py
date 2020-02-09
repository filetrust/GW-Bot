from gw_bot.api.Slack_Commands_Helper import Slack_Commands_Helper
from gw_bot.api.commands.GW_Commands import GW_Commands
from gw_bot.helpers.Lambda_Helpers import slack_message


def run(event, context):
    data    = event.get('data', {})
    params  = event.get('params', [])
    channel = data.get('channel')
    user    = data.get('user')
    text, attachments = Slack_Commands_Helper(GW_Commands).invoke(team_id=user, channel=channel, params=params)
    if channel:
        return None
    return text, attachments
    #channel = Misc.get_value(slack_event, 'channel')
    #user = Misc.get_value(slack_event, 'user')
    #
    slack_message(f':point_right: in commands: {event}',[],'DRE51D4EM')