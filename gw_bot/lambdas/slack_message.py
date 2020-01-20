def run(event, context):
    from gw_bot.api.API_OSS_Bot import API_OSS_Bot
    api = API_OSS_Bot()
    return api.send_message(event.get('channel'), event.get('text'), event.get('attachments'))