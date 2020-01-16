from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.S3 import S3
from pbx_gs_python_utils.utils.Files import Files

from gw_bot.api.gw.Glasswall import Glasswall


class API_Glasswall:

    def __init__(self):
        self.path_engine    = '/tmp/libglasswall.classic.so'
        self.path_output    = '/tmp/output'
        self.path_config    = './gw_bot/lambdas/gw/config.xml'
        self.glasswall      = None

    def setup(self):
        if self.glasswall is None:
            if True or Files.not_exists(self.path_engine):                                                                   # todo: there is some weird issue that happens if we don't download the file with every request
                S3().file_download_to('gw-bot-lambdas', 'lambdas-dependencies/libglasswall.classic.so', self.path_engine)

            self.glasswall = Glasswall(self.path_engine)             # load Glasswall engine
        return self


    def scan_file(self):
        xml_report = self.run_analysis_audit()
        return self.xml_to_json(xml_report)

    def xml_to_json(self, xml_report):
        gw_report = Lambda('gw_bot.lambdas.gw.gw_report')
        return gw_report.invoke({'xml_report':xml_report , 'report_type' :  'summary' })

    def run_analysis_audit(self):

        path_test_file = '/tmp/logo192.png'
        Files.folder_create(self.path_output)
        S3().file_download_to('gw-tf.com', 'logo192.png', path_test_file)

        self.glasswall.GWFileConfigXML(Files.contents(self.path_config))                         # load config file

        result = self.glasswall.GWFileAnalysisAudit(path_test_file, 'png')                  # analyse file

        return result.fileBuffer.decode()