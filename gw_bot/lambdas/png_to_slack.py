import base64

from osbot_aws.Dependencies import load_dependency
from osbot_aws.apis.S3               import S3
from osbot_aws.apis.Secrets          import Secrets
from osbot_aws.apis.shell.Lambda_Shell import lambda_shell
from osbot_utils.utils.Files import Files


def send_file_to_slack(file_path, title, bot_token, channel):                  # refactor into Slack_API class

    load_dependency('requests')          ;   import requests

    my_file = {
        'file': ('/tmp/file.png', open(file_path, 'rb'), 'png')
    }

    payload = {
        "filename"  : '{0}.png'.format(title),
        "token"     : bot_token,
        "channels"  : [channel],
    }
    requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)

    return 'send png file: {0}'.format(title)

@lambda_shell
def run(event, context):

    channel         = event.get('channel')
    png_data        = event.get('png_data')
    s3_bucket       = event.get('s3_bucket')
    s3_key          = event.get('s3_key')
    title           = event.get('title')

    #slack_message(':point_right: in png_to_slack', channel=channel)

    aws_secrets_id = 'slack-bot-oauth'
    bot_token       = Secrets(aws_secrets_id).value()

    if png_data:
        #(fd, tmp_file) = tempfile.mkstemp('png')
        tmp_file = Files.temp_file('.png')
        with open(tmp_file, "wb") as fh:
            fh.write(base64.decodebytes(png_data.encode()))
    else:
        if s3_bucket and s3_key:
            tmp_file = S3().file_download_and_delete(s3_bucket, s3_key)
        else:
            return None

    result = send_file_to_slack(tmp_file, title, bot_token, channel)

    #slack_message(':point_right: file sent to slack', channel=channel)
    return result
