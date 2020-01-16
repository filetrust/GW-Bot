import base64

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
            if Files.not_exists(self.path_engine):                                                                   # todo: there is some weird issue that happens if we don't download the file with every request
                S3().file_download_to('gw-bot-lambdas', 'lambdas-dependencies/libglasswall.classic.so', self.path_engine)

            self.glasswall = Glasswall(self.path_engine)             # load Glasswall engine
        return self


    def get_file_base_64(self, file_path):
        file_name = Files.file_name(file_path)

        with open(file_path, "rb") as file:
            raw_data = file.read()

        base64_data = base64.b64encode(raw_data).decode()
        return file_name, base64_data

    def scan_file(self, target_file):
        xml_report = self.run_analysis_audit(target_file)
        return self.xml_to_json(xml_report)

    def scan_file__base_64(self, file_name, file_contents):
        temp_file = Files.temp_file(Files.file_extension(file_name))
        with open(temp_file, "wb") as fh:
            fh.write(base64.decodebytes(file_contents.encode()))
        #path_file = save_file_to_disk(file_name, file_contents)
        return self.scan_file(temp_file)


    def xml_to_json(self, xml_report):
        gw_report = Lambda('gw_bot.lambdas.gw.gw_report')
        return gw_report.invoke({'xml_report':xml_report , 'report_type' :  'summary' })

    def run_analysis_audit(self, target_file):
        file_extension = Files.file_extension(target_file).replace('.','')
        self.glasswall.GWFileConfigXML(Files.contents(self.path_config))                 # load config file
        result = self.glasswall.GWFileAnalysisAudit(target_file, file_extension)         # analyse file
        return result.fileBuffer.decode()