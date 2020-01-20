from osbot_aws.apis.Lambda  import Lambda
from osbot_aws.apis.Secrets import Secrets
from pbx_gs_python_utils.utils.Files import Files
from slack                  import WebClient



class API_Slack:
    def __init__(self, channel = 'CSK9RADE2', team_id = None):      # 'gwbot-tests'
        self.bot_token = self.resolve_bot_token(team_id) #Secrets('slack-gs-bot').value()
        self.channel   = channel
        self.slack     = WebClient(self.bot_token)

    def resolve_bot_token(self,team_id):
        if team_id == 'T7F3AUXGV':    return Secrets('slack-gs-bot'       ).value()
        if team_id == 'T0SDK1RA8':    return Secrets('slack-gsbot-for-pbx').value()

        return Secrets('slack-gs-bot').value()

    # todo: commented files need refactoring to new API

    def add_reaction(self, ts, reaction):
        return self.slack.reactions_add(channel =self.channel, name = reaction , timestamp=ts)
        #return self.slack.api_call( "reactions.add", channel =self.channel, name = reaction , timestamp=ts )

    # def team_logins(self, count = 100, pages = 1):
    #     logins = []
    #     for page in range(1,pages + 1):
    #         data  = self.slack.api_call('team.accessLogs', count = count, page = page)
    #         entries = data.get('logins')
    #         #print('[API Slack][team_logins] got {0} entries for page {1}'.format(len(entries), page))
    #         logins.extend(entries)
    #     return logins

    # def channels_history(self,channel):
    #     return self.slack.api_call("channels.history", channel = channel)

    #def channels_public(self):
    #     channels = {}
    #     cursor = None
    #     while cursor != '':
    #         data = self.slack.channels_list("channels.list", cursor=cursor)
    #         data = self.slack.api_call("channels.list", cursor = cursor)
    #         cursor = data.get('response_metadata').get('next_cursor')
    #         for channel in data['channels']:
    #             channels[channel['name']] = channel
    #     return channels

    # def channels_private(self):
    #     channels = {}
    #     for channel in self.slack.api_call("conversations.list", types='private_channel')['channels']:
    #         channels[channel['name']] = channel
    #     return channels

    # def delete_message(self,ts):
    #     return self.slack.api_call("chat.delete", channel=self.channel,ts=ts)

    def files_info(self, file_id):
        #files.info
        return self.slack.files_info(file=file_id).data

    def get_channel(self, channel):
        return self.slack.api_call("channels.info", channel=channel)

    # def get_messages(self,channel,limit=10):
    #     messages = self.slack.api_call("conversations.history", channel=channel, limit=limit).get('messages')
    #     return [message.get('text') for message in messages]

    def send_message(self, text, attachments = None, channel = None):
        if attachments is None:
            attachments = []
        if channel is None:
            channel = self.channel
        return self.slack.chat_postMessage(channel=channel,text=text, attachments=attachments).data
        # return self.slack.api_call("chat.postMessage",
        #                     channel     = channel,
        #                     text        = text ,
        #                     attachments = attachments)

    def set_channel(self, channel):
        self.channel = channel
        return self

    # def user(self,used_id):
    #     return self.slack.api_call("chat.postMessage",
    #                                channel=self.channel,
    #                                used_  =used_id)
    #
    # def users(self):
    #     users = {}
    #     cursor = None
    #     while cursor != '':
    #         data = self.slack.api_call("users.list", cursor = cursor )
    #         cursor = data.get('response_metadata').get('next_cursor')
    #         for user in data.get('members'):
    #             users[user['name']] = user
    #     return users


    ## methods using lambdas

    # def dot_to_slack(self, dot):
    #     payload = {"dot"    : dot          ,
    #                "channel": self.channel }
    #     return Lambda('utils.dot_to_slack').invoke(payload)
    #
    # def puml_to_slack(self, puml):
    #     payload = {"puml"   : puml          ,
    #                "channel": self.channel  }
    #     return Lambda('utils.puml_to_slack').invoke(payload)


    # at the moment this is using the REST API directly (see if there is a way to do this using the main Slack python API)

    def upload_file(self, file_path, channel, title=None):
            import requests
            file_name       = Files.file_name(file_path)
            file_extension  = Files.file_extension(file_path)
            if title is None: title = file_name
            my_file        = {  'file': ('/tmp/file.png', open(file_path, 'rb'), file_extension) }

            payload        = {  "filename"  : '{0}.png'.format(title),
                                "token"     : self.bot_token         ,
                                "channels"  : [channel]              }
            requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)

            return 'file sent to slack {0}'.format(file_path)

