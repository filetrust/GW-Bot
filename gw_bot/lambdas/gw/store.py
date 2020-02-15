#todo: refactor to inside the store folder
def run(event, context):
    from gw_bot.api.Slack_Commands_Helper import Slack_Commands_Helper
    from gw_bot.api.commands.gw.store.Store_Commands import Store_Commands
    params  = event.get('params',{})
    data    = event.get('data'  ,{})
    channel = data.get('channel')

    result,_ = Slack_Commands_Helper(Store_Commands).invoke(channel=channel, params=params)
    if channel is None:
        return result
    return result