from pbx_gs_python_utils.utils.Json import Json
from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Misc import Misc
from pbx_gs_python_utils.utils.slack.Slack_Commands_Helper import Slack_Commands_Helper

from gw_bot.api.commands.GW_Commands           import GW_Commands
from gw_bot.api.commands.Maps_Commands         import Maps_Commands
from gw_bot.api.commands.Dev_Commands          import Dev_Commands
from gw_bot.api.commands.Participant_Commands  import Participant_Commands
from gw_bot.api.commands.Schedule_Commands     import Schedule_Commands
from gw_bot.api.commands.Sessions_Commands     import Sessions_Commands
from gw_bot.api.commands.Site_Commands         import Site_Commands
from gw_bot.api.commands.FAQ_Commands          import FAQ_Commands

def use_command_class(slack_event, params, target_class):
    channel = Misc.get_value(slack_event, 'channel')
    user    = Misc.get_value(slack_event, 'user')
    Slack_Commands_Helper(target_class).invoke(team_id=user, channel=channel, params=params)
    return None,None

class OSS_Bot_Commands:                                      # move to separate class

    gsbot_version = 'v0.17 (GW Bot)'

    @staticmethod
    def browser(slack_event=None, params=None):
        Lambda('osbot_browser.lambdas.lambda_browser').invoke_async({'params':params, 'data':slack_event}),[]
        return None,None

    # @staticmethod
    # def dev(slack_event=None, params=None):
    #     return use_command_class(slack_event, params, Dev_Commands)

    @staticmethod
    def gw(slack_event=None, params=None):
        # from osbot_aws.Globals import Globals
        # Globals.aws_session_region_name = 'eu-west-2'
        # from osbot_aws.apis.Lambda import Lambda
        # aws_lambda = Lambda('get_test_list')
        # payload = {}
        # import boto3
        # aws_lambda._boto_lambda = boto3.client('lambda', region_name='eu-west-2')
        # import json
        # response = aws_lambda.boto_lambda().invoke(FunctionName='get_test_list', Payload=json.dumps(payload))
        # result_bytes = response.get('Payload').read()
        # result_string = result_bytes.decode('utf-8')
        # result = json.loads(result_string).get('body')
        # return result,None
        # # arn:aws:lambda:eu-west-2:311800962295:function:get_test_list
        # # arn:aws:lambda:eu-west-1:311800962295:function:get_test_list'
        # #return
        # #result = aws_lambda.invoke()
        #
        # return f"test 1123 {json.dumps(response)}", None
        #
        #
        #
        # from osbot_aws.Globals import Globals
        #
        #
        #
        # return "test: {0}".format(aws_lambda.invoke()),None

        return use_command_class(slack_event, params, GW_Commands)
        #return '.....testing gw command..', None

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
    def hello_v2(slack_event=None, params=None):
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

    @staticmethod
    def site(slack_event=None, params=None):
        return use_command_class(slack_event, params, Site_Commands)

    @staticmethod
    def faq(slack_event=None, params=None):
        return use_command_class(slack_event, params, FAQ_Commands)

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




