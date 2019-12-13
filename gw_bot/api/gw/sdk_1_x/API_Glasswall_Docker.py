#rm -rf tmp-output;
# #docker run --rm -v /tmp/tmp-input:/home/classic_cli/input -v /tmp/tmp-output/:/home/classic_cli/output -v /tmp/tmp-config:/home/classic_cli/config safiankhan/glasswallclassic:2.0
# ./glasswallCLI -config=./config/config.ini -xmlconfig=./config/config.xml ;
#
# cat tmp-output/glasswallCLIProcess.log
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Process import Process

class API_Docker_Glasswall:
    def __init__(self):
        self.docker_image = "safiankhan/glasswallclassic:2.0"
        self.docker_cwd   = '/tmp'
        self.tmp_input    = '/tmp/tmp-input'
        self.tmp_output   = '/tmp/tmp-output'
        self.tmp_config   = '/tmp/tmp-config'


    def docker_exec(self, params):
        result = Process.run('docker', params, self.docker_cwd)
        if result.get('stderr'):
            return result.get('stderr')
        return result.get('stdout')

    def docker_run_bash_command(self, command):
        params = ['run', '--rm', self.docker_image]
        params.extend(command)
        return self.docker_exec(params)

    def glasswall_cli(self, command):
        params = ['run', '--rm',
                         '-v', self.tmp_input  + ':/home/classic_cli/input' ,
                         '-v', self.tmp_output + ':/home/classic_cli/output',
                         '-v', self.tmp_config + ':/home/classic_cli/config',
                         self.docker_image                                  ,
                        './glasswallCLI'
                  ]
        params.extend(command)
        return self.docker_exec(params)

    def glasswall_scan(self):
        command = ['-config=./config/config.ini', '-xmlconfig=./config/config.xml']
        return self.glasswall_cli(command)

    def scan_file(self, file_input, file_output=None, config_ini=None, config_xml=None):
        if config_ini is None: config_ini = default_config_ini
        if config_xml is None: config_xml = default_config_xml
        result = self.scan_file_with_config(file_input, config_ini, config_xml)
        if file_output and Files.exists(result.get('new_file')):
            Files.copy(result.get('new_file'), file_output)
        return result


    def scan_file_with_config(self, file, config_ini, config_xml):
        tmp_folder      = Files.temp_folder(parent_folder='/tmp')
        self.docker_cwd = tmp_folder
        self.tmp_input  = Files.folder_create(f'{tmp_folder}/input')
        self.tmp_output = Files.folder_create(f'{tmp_folder}/output')
        self.tmp_config = Files.folder_create(f'{tmp_folder}/config')

        Files.copy(file, self.tmp_input)
        Files.write(f'{self.tmp_config}/config.ini', config_ini)
        Files.write(f'{self.tmp_config}/config.xml', config_xml)

        scan_results = self.glasswall_scan()
        if 'SUCCESS' in scan_results:
            new_file     = Files.find(f'{tmp_folder}/output/Managed/**').pop()
        else:
            new_file = None
        return { 'new_file' : new_file, 'scan_results': scan_results}


    def watermark_file(self, file_input, file_output, watermark):
        config_ini = default_config_ini
        config_xml = default_config_xml.replace('<watermark>Glasswall</watermark>', f'<watermark>{watermark}</watermark>')
        return self.scan_file(file_input, file_output, config_ini, config_xml)

default_config_ini = """[GWConfig]
processMode=1
reportMode= 0
fileStorageMode=2
fileType=*
inputLocation= input
useSubfolders=1
outputLocation=output
createOutputFolders=1
nonConformingDirName= NonConforming
managedDirName= Managed
quarantineNonconforming= 1
writeOutput= 1
logFileSize=1
logFileProcessTime=1
logProcessStatus=0
"""

default_config_xml = """<?xml version="1.0" encoding="UTF-8"?>
<config>
    <pdfConfig>
		<watermark>Glasswall</watermark>
		<metadata>sanitise</metadata>
		<javascript>sanitise</javascript>
		<acroform>sanitise</acroform>
		<actions_all>sanitise</actions_all>
		<embedded_files>sanitise</embedded_files>
		<external_hyperlinks>sanitise</external_hyperlinks>
		<internal_hyperlinks>sanitise</internal_hyperlinks>
		<embedded_images>sanitise</embedded_images>
    </pdfConfig>
    <wordConfig>
		<metadata>sanitise</metadata>
		<macros>sanitise</macros>
		<embedded_files>sanitise</embedded_files>
		<review_comments>sanitise</review_comments>
		<internal_hyperlinks>sanitise</internal_hyperlinks>
		<external_hyperlinks>sanitise</external_hyperlinks>
		<dynamic_data_exchange>sanitise</dynamic_data_exchange>
		<embedded_images>sanitise</embedded_images>
    </wordConfig>
    <pptConfig>
		<metadata>sanitise</metadata>
		<macros>sanitise</macros>
		<embedded_files>sanitise</embedded_files>
		<review_comments>sanitise</review_comments>
		<internal_hyperlinks>sanitise</internal_hyperlinks>
		<external_hyperlinks>sanitise</external_hyperlinks>
		<embedded_images>sanitise</embedded_images>
    </pptConfig>
    <xlsConfig>
		<metadata>sanitise</metadata>
		<macros>sanitise</macros>
		<embedded_files>sanitise</embedded_files>
		<internal_hyperlinks>sanitise</internal_hyperlinks>
		<external_hyperlinks>sanitise</external_hyperlinks>
		<review_comments>sanitise</review_comments>
		<dynamic_data_exchange>sanitise</dynamic_data_exchange>
		<embedded_images>sanitise</embedded_images>
    </xlsConfig>	
</config>

"""