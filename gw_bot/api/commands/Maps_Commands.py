from osbot_aws.apis.Lambda import Lambda

class Maps_Commands:

    @staticmethod
    def ping(*event):
        return 'pong : {0}'.format(event)

    @staticmethod
    def create(*event):
        aws_lambda = Lambda('osbot_browser.lambdas.lambda_browser')
        params = ["maps", "exec_js"]
        params.extend(event[2])

        payload = {"params": params,
                   'data': {'channel': event[1]}}
        aws_lambda.invoke_async(payload)

    @staticmethod
    def cup_of_tea(*event):
        aws_lambda = Lambda('osbot_browser.lambdas.lambda_browser')
        payload = {"params": ["maps", "render", "cup-of-tea"],
                   'data': {'channel': event[1]}}
        aws_lambda.invoke_async(payload)

    @staticmethod
    def template(*event):
        aws_lambda = Lambda('osbot_browser.lambdas.lambda_browser')
        payload = {"params": ["maps", "default"],
                   'data': {'channel': event[1]}}
        aws_lambda.invoke_async(payload)




