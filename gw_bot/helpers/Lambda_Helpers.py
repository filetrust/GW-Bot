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

# ## todo: THIS NEEDED UPDATING
# def slack_message(text, attachments = [], channel = 'GDL2EC3EE', team_id='T7F3AUXGV'):  # GBMGMK88Z is the 'from-aws-lambda' channel in the GS-CST Slack workspace
#     payload = {
#                 'text'        : text        ,
#                 'attachments' : attachments ,
#                 'channel'     : channel     ,
#                 'team_id'     : team_id
#               }
#     Lambda('gw_bot.lambdas.slack_message').invoke_async(payload)


# def send_file_to_slack(file_path, title, bot_token, channel):
#     import requests
#     my_file = { 'file': ('/tmp/file.png', open(file_path, 'rb'), Files.file_extension(file_path)) }
#
#     payload = {
#         "filename"  : '{0}.png'.format(title),
#         "token"     : bot_token,
#         "channels"  : [channel],
#     }
#     requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)
#
#     return 'sent png file: {0}'.format(title)

def slack_message(text, attachments = None, channel = 'GDL2EC3EE', team_id='T7F3AUXGV'):  # GBMGMK88Z is the 'from-aws-lambda' channel in the GS-CST Slack workspace
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

