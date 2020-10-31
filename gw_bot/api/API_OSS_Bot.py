import json
import ssl
import urllib

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.Secrets import Secrets
from gw_bot.api.commands.OSS_Bot_Commands import OSS_Bot_Commands
from osbot_aws.helpers.Lambda_Helpers import log_to_elk, slack_message, log_error


class API_OSS_Bot:
    def __init__(self):
        self.slack_url   = "https://slack.com/api/chat.postMessage"
        self.bot_name    = '@ossbot'
        self.team_id     = 'TAULHPATC'
        self.bot_id      = '<@UAULZ1T98>'
        self.secret_name = 'slack-bot-oauth'
        self.bot_token   = self.resolve_bot_token()


    def resolve_bot_token(self):
        return Secrets(self.secret_name).value()

    def resolve_command_method(self, command):
        try:
            method_name = command.split(' ')[0].split('\n')[0].lower()
            return getattr(OSS_Bot_Commands,method_name)
        except:
            return None

    def handle_command(self, slack_event):
        try:
            attachments = []

            if slack_event.get('text'):
                #original = slack_event.get('text')
                command = slack_event.get('text').replace('<@URS8QH4UF>', '').strip()          # URS8QH4UF is the gw_bot slack ids

                command = command.replace('\u00a0',' ')  # fix prob caused by copy and paste inside slack, note: ".encode('ascii','ignore').decode()" didn't work because we lost the space

                if not command:
                    command = 'hello'

                if command.startswith('graph_') and len(command)==9:        # todo: move special cases to different method
                    command = f'graph show {command}'                       # in this case we are allowing the Slack user to just type a name of graph to see it

                method_name = command.split(' ')[0].split('\n')[0]

                method             = self.resolve_command_method(command)                        # find method to invoke
                if method:
                    method_params      = command.split(' ')[1:]
                    (text,attachments) = method(slack_event,method_params)                       # invoke method
                else:
                    text = ":exclamation: GW bot command `{0}` not found. Use `gw_bot help` to see a list of available commands".format(method_name)
                    log_error('Bad Command', {"text": text})
            #elif slack_event.get('subtype') == 'file_share':
            #    text = f":point_right: Hi you dropped the file ```{json.dumps(slack_event.get('files'), indent=2)}```"
            else:
                return None, None

        except Exception as error:
            text = '*GW Bot command execution error in `handle_command` :exclamation:*'
            attachments = [ { 'text': ' ' + str(error) , 'color' :  'danger'}]
            log_error(text, attachments)
        return text, attachments

    def process_posted_body(self, post_body):  # handle the encoding created by API GW, which uses as transformation
        try:                                  # { "body" : $input.json('$' ) }
            return_value = Lambda('gw_bot.lambdas.slack_callback').invoke(post_body)
            slack_message(f'return value: {return_value}')
            return return_value
        except Exception as error:
            return "Error in processing posted data: {0}".format(str(error))

    def handle_file_drop(self, slack_event):
        from osbot_aws.apis.Lambda import Lambda
        Lambda('gw_bot.lambdas.gw.gw_slack_file').invoke_async(slack_event)
        # text = f':point_right: the user {user_id} on the channel {channel} dropped the file ```f{json.dumps(file_info,indent=2) }```'
        # api_slack.send_message(text, channel=channel)
        # log_to_elk('file info', {'text':text})
        return None,None


    def process_event(self, slack_event):
        log_to_elk('GW Bot Slack Message', slack_event)
        attachments = []
        try:
            event_type            = slack_event.get('type')

            if    event_type == 'message'     : (text,attachments)  = self.handle_command    (slack_event )    # same handled
            elif  event_type == 'app_mention' : (text,attachments)  = self.handle_command    (slack_event )    # for these two events
            elif  event_type == 'file_created': (text,attachments)  = self.handle_file_drop  (slack_event )
            #elif  event_type == 'link_shared': (text,attachments)  = self.handle_link_shared(slack_event )    # special handler for jira links
            else:
                text = ':point_right: Unsupposed Slack bot event type: {0}'.format(event_type)
                log_error('Process Event', {'text': text})
        except Exception as error:
            text = '*OSS Bot command execution error in `process_event` :exclamation:*'
            attachments = [{'text': ' ' + str(error), 'color': 'danger'}]

        if text is None:
            return None, None

        channel_id = slack_event.get("channel")  # channel command was sent in
        if channel_id is None:
            return { "text": text, "attachments": attachments }
        return self.send_message(channel_id, text, attachments)


    def send_message(self,channel_id, text, attachments):
        data     = urllib.parse.urlencode((("token"      , self.bot_token  ),               # oauth token
                                           ("channel"    , channel_id      ),               # channel to send message to
                                           ("team_id"    , self.team_id    ),
                                           ("text"       ,  text            ),               # message's text
                                           ("attachments", json.dumps(attachments)     )))              # message's attachments
        data     = data.encode("ascii")
        request  = urllib.request.Request(self.slack_url, data=data, method="POST" ) # send data back to Slack
        request.add_header("Content-Type","application/x-www-form-urlencoded")
        context  = ssl.SSLContext()
        response = urllib.request.urlopen(request,context = context).read()
        return json.loads(response.decode())
