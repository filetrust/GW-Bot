from gw_bot.helpers.Lambda_Helpers import log_error, slack_message
from osbot_aws.Dependencies import load_dependency



def run(event, context):
    load_dependency('slack')
    load_dependency('requests')
    try:
        return          # disabled for now
        from gw_bot.api.gw.API_GW_Slack_File import API_GW_Slack_File
        api = API_GW_Slack_File()
        file_info = api.file_info_form_slack(event)
        #slack_message(f'{file_info}',[], 'DRE51D4EM')

        channel   = file_info.get('file').get('channels')[0]
        file_name = file_info.get('file').get('name')
        if file_name != 'scan.png':
            #slack_message(f'{file_info}',[], 'DRE51D4EM')
            slack_message(f':one: file upload detected, going to scan the *{file_name}* file with the GlassWall engine', [], channel)

            file_path = api.download_file(file_info)
            gw_report = api.gw_scan_file(file_path)
            api.send_report_to_slack(file_info, gw_report)

            return {'file_info': file_info , 'gw_report': gw_report }
    except Exception as error:
        message = f"[gw_slack_file] {error}"
        log_error('Error in Lambda', {'text': message})
        return {'error' : message}