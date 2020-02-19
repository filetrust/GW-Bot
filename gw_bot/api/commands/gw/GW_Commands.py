from gw_bot.helpers.Lambda_Helpers import slack_message
from osbot_aws.apis.Lambda import Lambda

from osbot_aws.apis.API_Gateway import API_Gateway


class GW_Commands:

    @staticmethod
    def ping (slack_id=None, channel=None, params=None) :
        return  'pong',None
