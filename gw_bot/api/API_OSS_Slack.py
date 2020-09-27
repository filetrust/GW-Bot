from osbot_aws.Dependencies import load_dependency


class API_OSS_Slack:
    def __init__(self):
        self._api_slack = None

    def api_slack(self):
        if self._api_slack is None:
            load_dependency('slack')
            from gw_bot.api.API_Slack import API_Slack
            self._api_slack = API_Slack()
        return self._api_slack

    def slack_id_to_slack_full_name(self,slack_id):
        data = self.api_slack().slack.users_info(user=slack_id)
        if data.get('ok') is True:
            return data.get('user').get('profile').get('real_name')