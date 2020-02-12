from gw_bot.helpers.Lambda_Helpers import slack_message
from osbot_aws.apis.API_Gateway import API_Gateway
from osbot_aws.apis.Lambda import Lambda


class Keys_Commands:

    @staticmethod
    def create(team_id,channel, params):
        key_name = ' '. join(params)
        if key_name == '':
            return slack_message(':red_circle: you need to provide a key name to create', [], channel)

        key_value = API_Gateway().api_key_create(key_name).get('value')
        return f'key `{key_name}` = {key_value}'

    @staticmethod
    def delete(team_id, channel, params):
        key_name = ' '.join(params)
        if key_name == '':
            return slack_message(':red_circle: you need to provide a key name to delete', [], channel)

        if API_Gateway().api_key_delete(key_name):
            return f':white_check_mark:  key deleted ok: `{key_name}`'
        return f':red_circle: could not delete key `{key_name}`. Does the key exists?'

    @staticmethod
    def list(team_id, channel, params):
        api_gateway = API_Gateway()
        result = ':point_down: Here are the current API Keys :point_down:\n'
        result += '```\n' + \
                  'Key id     | Key Name        | Key Value\n' + \
                  '-----------|-----------------|-----------------------------------------\n'
        for key_id, key_data in api_gateway.api_keys(include_values=True).items():
            result += f"{key_id:10} | {key_data.get('name'):15} | {key_data.get('value')}\n"
        result += '```'
        return slack_message(result, [], channel)

    @staticmethod
    def usage(slack_id=None, channel=None, params=None) :
        days        = 5
        title       = 'API Keys Usage'
        slack_message(f':point_right: Rendering chart with API Gateway Keys usage for the last `{days}` days', [], channel)
        chart_type  = 'LineChart'
        api_gateway = API_Gateway()
        usage_plans = api_gateway.usage_plans()
        plan_id     = set(usage_plans).pop()
        data        = api_gateway.usage__as_chart_data(plan_id,days)
        lambda_name = 'osbot_browser.lambdas.google_chart'
        options     = {'title'    : title,
                       'legend'   : {'position': 'bottom'}}

        params = { 'chart_type': chart_type, 'options': options , 'data': data }
        png_data = Lambda(lambda_name).invoke(params)

        if channel:
            params = {'png_data': png_data, 'title': 'API Keys usage chart', 'channel': channel}
            Lambda('utils.png_to_slack').invoke_async(params)
            return None
        else:
            return png_data