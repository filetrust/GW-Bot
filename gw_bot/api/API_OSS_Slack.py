from gw_bot.lambdas.png_to_slack import load_dependency


class API_OSS_Slack:
    def __init__(self):
        self._api_slack = None

    def api_slack(self):
        if self._api_slack is None:
            load_dependency('slack')
            from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
            self._api_slack = API_Slack()
        return self._api_slack

    def slack_id_to_slack_full_name(self,slack_id):

        #user_id = 'UAULZ1T98'

        data = self.api_slack().slack.api_call("users.info", user=slack_id)
        if data.get('ok') is True:
            return data.get('user').get('profile').get('real_name')