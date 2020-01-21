from gw_bot.helpers.Lambda_Helpers import log_error
from gw_bot.lambdas.png_to_slack import load_dependency



def run(event, context):
    load_dependency('slack')
    load_dependency('requests')
    try:
        from gw_bot.api.gw.API_GW_Slack_File import API_GW_Slack_File
        api = API_GW_Slack_File()
        file_info = api.file_info_form_slack(event)
        file_path = api.download_file(file_info)
        gw_report = api.gw_scan_file(file_path)

        api.send_report_to_slack(file_info, gw_report)

        return {'file_info': file_info , 'gw_report': gw_report }
    except Exception as error:
        message = f"[gw_slack_file] {error}"
        log_error('Error in Lambda', {'text': message})
        return {'error' : message}