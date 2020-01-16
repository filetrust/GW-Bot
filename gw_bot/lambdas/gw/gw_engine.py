#from osbot_aws.apis.S3 import S3
#from pbx_gs_python_utils.utils.Files import Files

from gw_bot.api.gw.API_Glasswall import API_Glasswall
#from gw_bot.api.gw.Glasswall import Glasswall


def run(event, context):

    return API_Glasswall().setup().scan_file()

    # path_config    = './gw_bot/lambdas/gw/config.xml'
    # path_engine    = '/tmp/libglasswall.classic.so'
    # path_test_file = '/tmp/logo192.png'
    # path_output    = '/tmp/output'
    #
    # Files.folder_create(path_output)
    # Files.write(path_test_file, 'contents')
    #
    # if True or Files.not_exists(path_engine):                                                                   # todo: there is some weird issue that happens if we don't download the file with every request
    #     s3 = S3()
    #     s3.file_download_to('gw-bot-lambdas', 'lambdas-dependencies/libglasswall.classic.so', path_engine)
    #     s3.file_download_to('gw-tf.com'     , 'logo192.png'                                 , path_test_file)
    #
    # gw = Glasswall(path_engine)                                             # load Glasswall engine
    # gw.GWFileConfigXML(Files.contents(path_config))                         # load config file
    #
    # result = gw.GWFileAnalysisAudit(path_test_file, 'png')                  # analyse file
    #
    # return result.fileBuffer.decode()                                       # return analysis as string




