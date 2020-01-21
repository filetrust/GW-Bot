import requests
from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Files import Files
from gw_bot.api.API_Slack import API_Slack
from gw_bot.api.gw.API_Glasswall import API_Glasswall
from gw_bot.helpers.Lambda_Helpers import log_to_elk


class API_GW_Slack_File:
    def __init__(self):
        self.api_slack = API_Slack()

    def file_info_form_slack(self, slack_event):
        file_id = slack_event.get('file_id')
        file_info = self.api_slack.files_info(file_id)
        return file_info

    def download_file(self, file_info):
        file_url      = file_info.get('file').get('url_private_download')
        file_name     = file_url.split('/').pop()
        tmp_file      = f'{Files.temp_folder("/tmp/")}/{file_name}'
        headers       = {'Authorization' : f"Bearer {self.api_slack.bot_token}"}
        file_contents = requests.get(file_url,headers=headers)

        with open(tmp_file, "wb") as fh:
           fh.write(file_contents.content)

        return tmp_file


    def gw_scan_file(self,target_file):
        (file_name, base64_data) = API_Glasswall().get_file_base_64(target_file)

        payload = {'file_contents': base64_data, 'file_name': file_name}

        return Lambda('gw_bot.lambdas.gw.gw_engine').invoke(payload)

    def send_report_to_slack(self, file_info, gw_report):
        channel   = file_info.get('file').get('channels').pop()
        file_name = file_info.get('file').get('name')
        file_id   = file_info.get('file').get('id')

        text      = f':point_right: Here is the Glasswall analysis for the file *{file_name}* with file id ({file_id}) '+ \
                    f'uploaded by the user <@{file_info.get("file").get("user")}> on channel <#{channel}> ' #+ \
                    #f'```{json.dumps(gw_report,indent=2)}```'

        channel = 'DRE51D4EM'                # for now override the message to sent the value as a DM to DinisCruz
        self.api_slack.send_message(text, channel=channel)

        #self.api_slack.upload_file('/tmp/test_file.png', channel)