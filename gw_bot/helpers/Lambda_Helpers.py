from osbot_aws.apis.Lambda import Lambda


def log_info(message, data = None, index = "gw_bot_logs",category = "API_GS_Bot"):
    return log_to_elk(message=message, data=data, index=index, level='info', category=category)

def log_debug(message, data=None, index="gw_bot_logs", category="API_GS_Bot"):
    return log_to_elk(message=message, data=data, index=index, level='debug', category=category)

def log_error(message, data = None, index = "gw_bot_logs", category = "API_GS_Bot"):
    return log_to_elk(message=message, data=data, index=index, level='error', category=category)

def log_to_elk(message, data = None, index = "gw_bot_logs", level = "debug", category = "API_GS_Bot"):
    payload = {
                "index"    : index    ,
                "level"    : level    ,
                "message"  : message  ,
                "category" : category ,
                "data"     : data
              }

    Lambda('gw_bot.utils.log_to_elk').invoke_async(payload)
    return payload

def slack_message(text, attachments = None, channel = None, team_id=None):  # GBMGMK88Z is the 'from-aws-lambda' channel in the GS-CST Slack workspace
    if attachments is None: attachments = []
    payload = {
                'text'        : text        ,
                'attachments' : attachments ,
                'channel'     : channel     ,
                'team_id'     : team_id
              }
    if channel:
        Lambda('pbx_gs_python_utils.lambdas.utils.slack_message').invoke_async(payload)
    else:
        return text, attachments


def screenshot_from_url(url):
    payload = {"params": ['screenshot', url]}
    return  Lambda('osbot_browser.lambdas.lambda_browser').invoke(payload)

