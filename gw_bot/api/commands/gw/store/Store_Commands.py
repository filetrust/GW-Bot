from gw_bot.api.Slack_Commands_Helper import Slack_Commands_Helper
#from gw_bot.helpers.Lambda_Helpers import slack_message
#from osbot_aws.apis.Lambda import Lambda
from gw_bot.api.commands.gw.store.Keys_Commands import Keys_Commands


class Store_Commands:

    @staticmethod
    def keys(team_id, channel, params):
        text,attachments = Slack_Commands_Helper(Keys_Commands).invoke(channel=channel, params=params)
        if channel is None:
            return text, attachments

    # def api_keys(team_id, channel, params):
    #     from osbot_aws.apis.API_Gateway import API_Gateway
    #     api_gateway = API_Gateway()
    #     result = ':point_down: Here are the current API Keys :point_down:\n'
    #     result += '```\n' + \
    #               'Key id     | Key Name        | Key Value\n' + \
    #               '-----------|-----------------|-----------------------------------------\n'
    #     for key_id, key_data in api_gateway.api_keys(include_values=True).items():
    #         result += f"{key_id:10} | {key_data.get('name'):15} | {key_data.get('value')}\n"
    #     result += '```'
    #     if channel:
    #         slack_message(result, [], channel)
    #     else:
    #         return result
    #     return 'returning api keys'