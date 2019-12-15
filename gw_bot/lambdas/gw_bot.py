def run(data, context):
    # this Lambda function is triggered by this API GW method https://545ojrb6r0.execute-api.eu-west-2.amazonaws.com/dev/event-handler
    try:
        from gw_bot.api.Slack_Handler import Slack_Handler
        return Slack_Handler().run(data)
    except Exception as error:
        return "500 Error: {0}".format(error)