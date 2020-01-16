from gw_bot.api.gw.API_Glasswall import API_Glasswall

def run(event, context):
    file_name     = event.get('file_name')
    file_contents = event.get('file_contents')

    return API_Glasswall().setup()                                          \
                          .scan_file__base_64(file_name, file_contents)




