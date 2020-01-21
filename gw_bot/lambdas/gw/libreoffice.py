import base64
import shutil

from osbot_aws.apis.S3 import S3
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Process import Process

def install_libreoffice():
    tmp_dir      = '/tmp'
    file_name    = 'instdir.zip'
    file_zip     = f'{tmp_dir}/{file_name}'
    bucket       = 'gw-bot-lambdas'
    s3_key       = f'lambdas-dependencies/{file_name}'
    unziped_path = f'{tmp_dir}/{file_name}'
    if Files.exists(unziped_path) is False:
        S3().file_download_to(bucket, s3_key, file_zip)
        shutil.unpack_archive(file_zip, extract_dir=tmp_dir)
    return unziped_path


def run(event, context):
    file_name = event.get('file_name')
    file_contents = event.get('file_contents')
    temp_file = Files.temp_file(Files.file_extension(file_name))
    with open(temp_file, "wb") as fh:
        fh.write(base64.decodebytes(file_contents.encode()))


    install_libreoffice()

    Process.run('chmod', ['+x', '/tmp/instdir/program/soffice.bin'])
    cmd    = "/tmp/instdir/program/soffice.bin"
    params = ["--headless", "--invisible", "--nodefault", "--nofirststartwizard",
              "--nolockcheck", "--nologo", "--norestore", "--convert-to pdf",
              "--outdir /tmp", 'temp_file']

    return Process.run(cmd, params, cwd='/tmp')
