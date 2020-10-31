from osbot_utils.decorators.Method_Wrappers import cache
from osbot_utils.utils.Files import path_combine
from osbot_utils.utils.Json import json_load

# not currently used
class GW_Bot_Config:

    def __init__(self):
        self.config_file = path_combine(__file__,'../../gw-bot-config.json')

    @cache
    def config(self):
        return  json_load(self.config_file)

    @cache
    def slack_allowed_users(self):
        return self.config().get('slack',{}).get('allowed_users')

    def version(self):
        return self.config().get('version')