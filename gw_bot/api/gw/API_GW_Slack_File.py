import json
import requests
from osbot_aws.apis.Lambda import Lambda
from gw_bot.api.API_Slack import API_Slack
from gw_bot.api.gw.API_Glasswall import API_Glasswall
from gw_bot.helpers.Lambda_Helpers import log_to_elk, slack_message
from osbot_utils.utils.Files import Files


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
        channel   = file_info.get('file').get('channels')[0]
        file_name = file_info.get('file').get('name')
        file_id   = file_info.get('file').get('id')

        text      = f':two: Scan of file *{file_id}* completed, generating report' #+ \
                    #f'```{json.dumps(gw_report,indent=2)}```'
                    # f'uploaded by the user <@{file_info.get("file").get("user")}> on channel <#{channel}> ' #+ \

        #channel = 'DRE51D4EM'                # for now override the message to sent the value as a DM to DinisCruz
        #self.api_slack.send_message(text, [], channel=channel)
        slack_message(text, [], channel=channel)
        from osbot_aws.apis.Lambda import Lambda
        file_name = file_info.get('file').get('name')
        payload = {'file_name': file_name, 'json_data': gw_report}
        png_data = Lambda('osbot_browser.lambdas.gw.xml_report').invoke(payload).get('png_data')
        if png_data is None:
            slack_message(':red_circle: report table could not be be created', [], channel=channel)
        else:
            slack_message(':three: report created, sending it to Slack', [], channel=channel)
            self.api_slack.upload_image_from_png_base64(png_data, channel, 'scan')

        #self.api_slack.upload_file('/tmp/test_file.png', channel)