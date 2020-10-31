from osbot_aws.helpers.Lambda_Helpers import log_debug

def run(event, context):
    try:
        #log_debug("in slack callback", f'{event}')
        from gw_bot.api.API_Slack_Integration import API_Slack_Interaction
        return API_Slack_Interaction().handle_request(event)

    except Exception as error:
        log_debug("Error processing request: {0}".format(error), data=event, category='gw_bot')
        return "500 Error: {0}".format(error)