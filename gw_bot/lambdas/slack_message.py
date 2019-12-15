def run(event, context):
    from gw_bot.api.API_OSS_Bot import API_OSS_Bot

    api = API_OSS_Bot()
    #api.send_message('DJ8UA0RFT', data.get('text'),[])
    #TAULHPATC
    api.send_message(event.get('channel'), event.get('text'), event.get('attachments'))
    #return 'this will be a slack message'