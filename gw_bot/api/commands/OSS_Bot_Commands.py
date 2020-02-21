from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Misc import Misc

from gw_bot.api.Slack_Commands_Helper          import Slack_Commands_Helper
from gw_bot.api.commands.Maps_Commands         import Maps_Commands


def use_command_class(slack_event, params, target_class):
    channel          = Misc.get_value(slack_event, 'channel')
    user             = Misc.get_value(slack_event, 'user')
    text,attachments =  Slack_Commands_Helper(target_class).invoke(team_id=user, channel=channel, params=params)
    if channel:
        return None,None
    return text,attachments

class OSS_Bot_Commands:                                      # move to separate class

    gsbot_version = 'v0.39 (GW Bot)'

    @staticmethod
    def aws(slack_event=None, params=None):
        Lambda('gw_bot.lambdas.aws.commands').invoke_async({'params': params, 'data': slack_event}), []
        return None, None

    @staticmethod
    def browser(slack_event=None, params=None):
        Lambda('osbot_browser.lambdas.lambda_browser').invoke_async({'params':params, 'data':slack_event}),[]
        return None,None

    # @staticmethod
    # def dev(slack_event=None, params=None):
    #     return use_command_class(slack_event, params, Dev_Commands)

    @staticmethod
    def gw(slack_event=None, params=None):
        #return use_command_class(slack_event, params, GW_Commands)
        Lambda('gw_bot.lambdas.gw.commands').invoke_async({'params': params, 'data': slack_event}), []
        return None, None

    @staticmethod
    def graph(slack_event, params=None):
        Lambda('osbot_jira.lambdas.graph').invoke_async({'params': params, 'data': slack_event}), []
        return None, None

    @staticmethod
    def jira(slack_event, params=None):
        Lambda('osbot_jira.lambdas.jira').invoke_async({"params" : params, "user": slack_event.get('user'), "channel": slack_event.get('channel'),
                                                                'team_id': slack_event.get('team_id')}, )
        return None, None
    @staticmethod
    def jp(slack_event=None, params=None):
        return OSS_Bot_Commands.jupyter(slack_event,params)

    @staticmethod
    def jupyter(slack_event=None, params=None):
        Lambda('osbot_jupyter.lambdas.osbot').invoke_async({'params': params, 'data': slack_event}), []
        return None, None

    @staticmethod
    def hello(slack_event=None, params=None):
        user = Misc.get_value(slack_event, 'user')
        return 'Hello <@{0}>, how can I help you?'.format(user), []

    @staticmethod
    def help(*params):
        commands        = [func for func in dir(OSS_Bot_Commands) if callable(getattr(OSS_Bot_Commands, func)) and not func.startswith("__")]
        title           = "*Here are the commands available*"
        attachment_text = ""
        for command in commands:
            if command is not 'bad_cmd':
                attachment_text += " • {0}\n".format(command)
        return title,[{'text': attachment_text, 'color': 'good'}]

    @staticmethod
    def screenshot(slack_event=None, params=None):
        params.insert(0,'screenshot')
        Lambda('osbot_browser.lambdas.lambda_browser').invoke_async({'params': params, 'data': slack_event}), []
        return None, None

    # @staticmethod
    # def site(slack_event=None, params=None):
    #     return use_command_class(slack_event, params, Site_Commands)

    @staticmethod
    def store(slack_event=None, params=None):
        Lambda('gw_bot.lambdas.gw.store.commands').invoke_async({'params': params, 'data': slack_event}), []
        return None, None

    # @staticmethod
    # def faq(slack_event=None, params=None):
    #     return use_command_class(slack_event, params, FAQ_Commands)

    @staticmethod
    def maps(slack_event=None, params=None):
        return use_command_class(slack_event, params, Maps_Commands)

    # @staticmethod
    # def participant(slack_event=None, params=None):
    #     return use_command_class(slack_event,params,Participant_Commands)
    #
    # @staticmethod
    # def schedule(slack_event=None, params=None):
    #     return use_command_class(slack_event, params, Schedule_Commands)
    #
    # @staticmethod
    # def sessions(slack_event=None, params=None):
    #     return use_command_class(slack_event, params, Sessions_Commands)

    @staticmethod
    def version(*params):
        return OSS_Bot_Commands.gsbot_version,[]




