from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Lambda_Helpers import slack_message

from gw_bot.api.API_OSS_Slack import API_OSS_Slack


def send_screenshot_to_slack(path, channel, extra_params: list):
    if path is None: path = ''
    url = 'https://open-security-summit.org/' + path
    from gw_bot.api.commands.OSS_Bot_Commands import OSS_Bot_Commands
    params = ["screenshot", url]
    params.extend(extra_params)
    OSS_Bot_Commands().browser({'channel': channel}, params)



class Participant_Commands:

    @staticmethod
    def me(slack_id=None, channel=None, params=None):

        name = API_OSS_Slack().slack_id_to_slack_full_name(slack_id)
        return Participant_Commands.view(slack_id, channel, [name])

    @staticmethod
    def info(team_id=None, channel=None, params=None):
        name = " ".join(params)
        aws_lambda = Lambda('gw_bot.lambdas.git_lambda')
        payload = {'action' : 'participant_info' ,
                   'name'   : name               ,
                   'channel': channel            ,
                   'commit' : False              }
        aws_lambda.invoke_async(payload)

    @staticmethod
    def view(team_id=None, channel=None, params=None):
        name = " ".join(params)
        aws_lambda = Lambda('gw_bot.lambdas.git_lambda')
        payload = {'action': 'participant_url',
                   'name'  : name,
                   'commit': False}
        result = aws_lambda.invoke(payload)
        if result.get('status') == 'ok':
            path = result.get('data')
            send_screenshot_to_slack(path,channel,[1200])
        else:
            slack_message(":red_circle: Sorry, couldn't find url for `{0}`".format(name),[],channel)
            return ":red_circle: Sorry, couldn't find url for `{0}`".format(name)


    @staticmethod
    def edit(team_id=None, channel=None, params=None):
        data = " ".join(params).split(',')
        if len(data) != 3:
            return "error: you need to provide 3 fields to edit the value(comma delimited): `name`, `field name` and `field value`"
        name, field, value = data
        name  = name.strip()
        field = field.strip()
        value = value.strip()
        aws_lambda = Lambda('gw_bot.lambdas.git_lambda')
        payload = {'action' : 'participant_edit_field',
                   'name'   : name,
                   'channel': channel,
                   'field' : field,
                   'value': value}
        aws_lambda.invoke_async(payload)

    @staticmethod
    def append(team_id=None, channel=None, params=None):
        data = " ".join(params).split(',')
        if len(data) != 3:
            return "error: you need to provide 3 fields to append an value (comma delimited): `name`, `field name` and `field value`"
        name, field, value = data
        name = name.strip()
        field = field.strip()
        value = value.strip()
        aws_lambda = Lambda('gw_bot.lambdas.git_lambda')
        payload = {'action': 'participant_append_to_field',
                   'name': name,
                   'channel': channel,
                   'field': field,
                   'value': value}
        aws_lambda.invoke_async(payload)

    @staticmethod
    def remove(team_id=None, channel=None, params=None):
        data = " ".join(params).split(',')
        if len(data) != 3:
            return "error: you need to provide 3 fields to append an value (comma delimited): `name`, `field name` and `field value`"
        name, field, value = data
        name = name.strip()
        field = field.strip()
        value = value.strip()
        aws_lambda = Lambda('gw_bot.lambdas.git_lambda')
        payload = {'action': 'participant_remove_from_field',
                   'name': name,
                   'channel': channel,
                   'field': field,
                   'value': value}
        aws_lambda.invoke_async(payload)


