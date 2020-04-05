from osbot_aws.apis.S3 import S3
from osbot_utils.utils.Files import file_exists, save_string_as_file, file_not_exists
from osbot_utils.utils.Http import GET, GET_bytes_to_file
from osbot_utils.utils.Process import Process

path_dot_static = '/tmp/dot_static'

def setup():
    #using file from https://github.com/restruct/dot-static/blob/master/x64/dot_static
    S3().file_download_to('gw-bot-lambdas', 'lambdas-dependencies/dot_static', path_dot_static)
    Process.run("chmod", ['+x', path_dot_static])


#note: when using these images you will also need to have the same files with same paths available locally
# def download_images(images):
#    if images:
#        for tmp_path, image_url in images.items():
#            if file_not_exists(tmp_path):
#                 GET_bytes_to_file(image_url, tmp_path)

# in run
#images        = event.get('images')
#download_images(images)


def run(event, context=None):
    dot_code      = event.get('dot')
    layout_engine = event.get('layout_engine', 'fdp')
    output_format = event.get('output_format', 'svg')

    setup()

    dot_file = save_string_as_file(dot_code)
    result   = Process.run('/tmp/dot_static',params=[dot_file, f'-T{output_format}',f'-K{layout_engine}'])
    if result.get('stderr'):
        return  {'error': result.get('stderr'), 'svg': result.get('stdout')}
    return {'svg': result.get('stdout')}
