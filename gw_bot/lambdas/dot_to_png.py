from osbot_aws.apis.S3 import S3
from osbot_utils.utils.Files import file_exists, save_string_as_file
from osbot_utils.utils.Process import Process

path_dot_static = '/tmp/dot_static'

def setup():
    #using file from https://github.com/restruct/dot-static/blob/master/x64/dot_static
    S3().file_download_to('gw-bot-lambdas', 'lambdas-dependencies/dot_static', path_dot_static)
    Process.run("chmod", ['+x', path_dot_static])

def run(event, context=None):
    setup()
    dot_code = event.get('dot')
    dot_file = save_string_as_file(dot_code)
    result   = Process.run('/tmp/dot_static',params=[dot_file, '-Tsvg'])
    if result.get('stderr'):
        return  {'error': result.get('stderr')}
    return {'svg': result.get('stdout')}
