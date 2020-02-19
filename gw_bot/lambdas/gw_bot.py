def run(data, context):    
    try:
        from gw_bot.api.Slack_Handler import Slack_Handler
        return Slack_Handler().run(data)
    except Exception as error:
        return "500 Error: {0}".format(error)