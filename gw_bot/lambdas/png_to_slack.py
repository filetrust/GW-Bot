import base64
from pbx_gs_python_utils.utils.Files import Files
from osbot_aws.apis.S3               import S3
from osbot_aws.apis.Secrets          import Secrets

def load_dependency(target):
    from osbot_aws.apis.S3 import S3
    import shutil
    import sys
    s3         = S3()
    s3_bucket  = 'gw-bot-lambdas'
    s3_key     = 'lambdas-dependencies/{0}.zip'.format(target)
    tmp_dir    = Files.path_combine('/tmp/lambdas-dependencies', target)
    #return s3.file_exists(s3_bucket,s3_key)

    if s3.file_exists(s3_bucket,s3_key) is False:
        raise Exception("In Lambda load_dependency, could not find dependency for: {0}".format(target))

    if Files.not_exists(tmp_dir):                               # if the tmp folder doesn't exist it means that we are loading this for the first time (on a new Lambda execution environment)
        zip_file = s3.file_download(s3_bucket, s3_key,False)    # download zip file with dependencies
        shutil.unpack_archive(zip_file, extract_dir = tmp_dir)  # unpack them
        sys.path.append(tmp_dir)                                # add tmp_dir to the path that python uses to check for dependencies
    return Files.exists(tmp_dir)

def upload_dependency(target):
    s3        = S3()
    s3_bucket = 'gw-bot-lambdas'
    s3_file   = 'lambdas-dependencies/{0}.zip'.format(target)
    path_libs = Files.path_combine('../../../_lambda_dependencies/', target)
    if Files.not_exists(path_libs):
        raise Exception("In Lambda upload_dependency, could not find dependency for: {0}".format(target))
    s3.folder_upload(path_libs, s3_bucket, s3_file)
    return s3.file_exists(s3_bucket, s3_file)

def send_file_to_slack(file_path, title, bot_token, channel):                  # refactor into Slack_API class


    #from osbot_aws.apis.Lambda import load_dependency


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


def run(event, context):

    channel         = event.get('channel')
    png_data        = event.get('png_data')
    s3_bucket       = event.get('s3_bucket')
    s3_key          = event.get('s3_key')
    title           = event.get('title')
    team_id         = event.get('team_id')
    #aws_secrets_id  = event.get('aws_secrets_id')
    #if  team_id == 'T7F3AUXGV': aws_secrets_id = 'slack-gs-bot'             # hard coded values
    #if  team_id == 'T0SDK1RA8': aws_secrets_id = 'slack-gsbot-for-pbx'      # need to move to special function
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

    return send_file_to_slack(tmp_file, title, bot_token, channel)
