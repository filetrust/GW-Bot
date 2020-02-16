from osbot_aws.apis.Lambda import Lambda


class AWS_Commands:

    @staticmethod
    def billing(team_id, channel, params):
        lambda_name = 'osbot_browser.lambdas.aws_web'
        Lambda(lambda_name).invoke({'channel': channel})

    @staticmethod
    def ping(team_id, channel, params):
        return 'pong'