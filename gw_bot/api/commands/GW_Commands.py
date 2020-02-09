from gw_bot.helpers.Lambda_Helpers import slack_message
from osbot_aws.apis.Lambda import Lambda

from osbot_aws.apis.API_Gateway import API_Gateway


class GW_Commands:

    @staticmethod
    def ping (slack_id=None, channel=None, params=None) :
        return  'pong',None

    @staticmethod
    def api_usage(slack_id=None, channel=None, params=None) :
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

    @staticmethod
    def api_keys(slack_id=None, channel=None, params=None) :
        api_gateway = API_Gateway()
        result = ':point_down: Here are the current API Keys :point_down:\n'
        result += '```\n' + \
                  'Key id     | Key Name   | Key Value\n' + \
                  '-----------|------------|-----------------------------------------\n'
        for key_id,key_data in api_gateway.api_keys(include_values=True).items():
            result += f"{key_id:10} | {key_data.get('name'):10} | {key_data.get('value')}\n"
        result += '```'
        if channel:
            slack_message(result,[], channel)
        else:
            return result

    # @staticmethod
    # def get_test_list(slack_id=None, channel=None, params=None) :
    #     from osbot_aws.Globals import Globals
    #     Globals.aws_session_region_name = 'eu-west-2'
    #     from osbot_aws.apis.Lambda import Lambda
    #     aws_lambda = Lambda('get_test_list')
    #     payload = {}
    #     import boto3
    #     aws_lambda._boto_lambda = boto3.client('lambda', region_name='eu-west-2')
    #     import json
    #     response = aws_lambda.boto_lambda().invoke(FunctionName='get_test_list', Payload=json.dumps(payload))
    #     result_bytes = response.get('Payload').read()
    #     result_string = result_bytes.decode('utf-8')
    #     result = json.loads(result_string).get('body')
    #     text = f":point_right: Here is the result from the execution of the `get_test_list` lambda function: \n```{result}``` "
    #     return text, None


        # Globals.aws_session_region_name = 'eu-west-2'
        #
        # from osbot_aws.apis.Lambda import Lambda
        #
        # aws_lambda = Lambda('get_test_list')
        # return "{0}".format(aws_lambda.invoke())

