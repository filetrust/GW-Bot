import requests
from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Files import Files
from gw_bot.api.API_Slack import API_Slack
from gw_bot.api.gw.API_Glasswall import API_Glasswall


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



        #user_id = slack_event.get('user_id')
        #channel = file_info.get('file').get('channels').pop()

        #text = f':point_right: the user {user_id} on the channel {channel} dropped the file ```f{json.dumps(file_info, indent=2)}```'
        #api_slack.send_message(text, channel=channel)
        #log_to_elk('file info', {'text': text})