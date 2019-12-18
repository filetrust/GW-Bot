

class GW_Commands:

    @staticmethod
    def ping (slack_id=None, channel=None, params=None) :
        return  'pong',None

    @staticmethod
    def get_test_list(slack_id=None, channel=None, params=None) :
        from osbot_aws.Globals import Globals
        Globals.aws_session_region_name = 'eu-west-2'
        from osbot_aws.apis.Lambda import Lambda
        aws_lambda = Lambda('get_test_list')
        payload = {}
        import boto3
        aws_lambda._boto_lambda = boto3.client('lambda', region_name='eu-west-2')
        import json
        response = aws_lambda.boto_lambda().invoke(FunctionName='get_test_list', Payload=json.dumps(payload))
        result_bytes = response.get('Payload').read()
        result_string = result_bytes.decode('utf-8')
        result = json.loads(result_string).get('body')
        text = f":point_right: Here is the result from the execution of the `get_test_list` lambda function: \n```{result}``` "
        return text, None


        # Globals.aws_session_region_name = 'eu-west-2'
        #
        # from osbot_aws.apis.Lambda import Lambda
        #
        # aws_lambda = Lambda('get_test_list')
        # return "{0}".format(aws_lambda.invoke())

