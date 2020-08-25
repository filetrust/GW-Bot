#rm -rf tmp-output;
# #docker run --rm -v /tmp/tmp-input:/home/classic_cli/input -v /tmp/tmp-output/:/home/classic_cli/output -v /tmp/tmp-config:/home/classic_cli/config safiankhan/glasswallclassic:2.0
# ./glasswallCLI -config=./config/config.ini -xmlconfig=./config/config.xml ;

#docker run --rm -v /tmp/tmp-input:/input -v /tmp/tmp-output/:/output -v /tmp/tmp-config:/config glasswallsolutions/evaluationsdk:2 GWQtCLI
#./glasswallCLI -config=./config/config.ini -xmlconfig=./config/config.xml ;
#
# cat tmp-output/glasswallCLIProcess.log


from gw_bot.api.gw.skd_editor.API_SISL import API_SISL
from osbot_utils.utils.Files import Files
from osbot_utils.utils.Process import Process


class API_Glasswall_Editor:
    def __init__(self):
        self.docker_image = "gw-editor-eval" #"glasswallsolutions/evaluationsdk:2"
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
                         '-v', self.tmp_input  + ':/input' ,
                         '-v', self.tmp_output + ':/output',
                         '-v', self.tmp_config + ':/config',
                         self.docker_image                                  ,
                        './GWQtCLI'
                  ]
        params.extend(command)
        return self.docker_exec(params)

    def glasswall_scan(self):
        command = ['-c','/config/config.xml','-i','/input','-o','/output']
        return self.glasswall_cli(command)

    def glasswall_export(self):
        command = ['-c','/config/config.xml','-i','/input','-o','/output', '-x','export']
        return self.glasswall_cli(command)

    def glasswall_import(self):
        command = ['-c','/config/config.xml','-i','/input','-o','/output', '-x','import']
        return self.glasswall_cli(command)

    def scan_file(self, file_input, file_output=None, config_xml=None):
        if config_xml is None: config_xml = default_config_xml
        result = self.scan_file_with_config(file_input, config_xml)
        if file_output and Files.exists(result.get('new_file')):
            Files.copy(result.get('new_file'), file_output)
        return result


    def scan_file_with_config(self, file, config_xml):
        file_name = Files.file_name(file)
        tmp_folder      = Files.temp_folder(parent_folder='/tmp')
        self.docker_cwd = tmp_folder
        self.tmp_input  = Files.folder_create(f'{tmp_folder}/input')
        self.tmp_output = Files.folder_create(f'{tmp_folder}/output')
        self.tmp_config = Files.folder_create(f'{tmp_folder}/config')

        Files.copy(file, self.tmp_input)
        Files.write(f'{self.tmp_config}/config.xml', config_xml)

        scan_results = self.glasswall_scan()
        #if 'SUCCESS' in scan_results:
        new_file = Files.find(f'{tmp_folder}/output/{file_name}').pop()
        #else:
        #    new_file = None
        return { 'new_file' : new_file, 'scan_results': scan_results}
    #
    #
    # def watermark_file(self, file_input, file_output, watermark):
    #     config_xml = default_config_xml.replace('<watermark>Glasswall</watermark>', f'<watermark>{watermark}</watermark>')
    #     return self.scan_file(file_input, file_output, config_xml)
    def file_to_sisl(self, file):
        config_xml = default_config_xml
        file_name  = Files.file_name(file)
        tmp_folder = Files.temp_folder(suffix='-'+file_name, parent_folder='/tmp')
        self.docker_cwd = tmp_folder
        self.tmp_input = Files.folder_create(f'{tmp_folder}/input')
        self.tmp_output = Files.folder_create(f'{tmp_folder}/output')
        self.tmp_config = Files.folder_create(f'{tmp_folder}/config')

        Files.copy(file, self.tmp_input)
        Files.write(f'{self.tmp_config}/config.xml', config_xml)

        self.glasswall_export()
        return f'{self.tmp_output}/{file_name}.zip'

    def sisl_to_file(self, sisl_file, target_file):
        config_xml = default_config_xml
        file_name = Files.file_name(sisl_file)
        tmp_folder = Files.temp_folder(suffix='-'+ file_name, parent_folder='/tmp')
        self.docker_cwd = tmp_folder
        self.tmp_input = Files.folder_create(f'{tmp_folder}/input')
        self.tmp_output = Files.folder_create(f'{tmp_folder}/output')
        self.tmp_config = Files.folder_create(f'{tmp_folder}/config')

        Files.copy(sisl_file, self.tmp_input)
        Files.write(f'{self.tmp_config}/config.xml', config_xml)

        self.glasswall_import()
        new_file = f'{tmp_folder}/output/{file_name.replace(".zip","")}'
        return Files.copy(new_file,target_file)


default_config_xml = """<?xml version="1.0" encoding="utf-8"?>
<config>
    <pdfConfig>
        <watermark>Glasswall Protected</watermark>
        <acroform>sanitise</acroform>
        <metadata>sanitise</metadata>
        <javascript>sanitise</javascript>
        <actions_all>sanitise</actions_all>
        <embedded_files>sanitise</embedded_files>
        <internal_hyperlinks>sanitise</internal_hyperlinks>
        <external_hyperlinks>sanitise</external_hyperlinks>
        <embedded_images>sanitise</embedded_images>
    </pdfConfig>
    <wordConfig>
       <macros>sanitise</macros>
        <metadata>sanitise</metadata>
        <embedded_files>sanitise</embedded_files>
        <embedded_images>sanitise</embedded_images>
        <review_comments>sanitise</review_comments>
        <internal_hyperlinks>sanitise</internal_hyperlinks>
        <external_hyperlinks>sanitise</external_hyperlinks>
        <dynamic_data_exchange>sanitise</dynamic_data_exchange>
    </wordConfig>
    <pptConfig>    
        <macros>sanitise</macros>
        <metadata>sanitise</metadata>
        <embedded_files>sanitise</embedded_files>
        <embedded_images>sanitise</embedded_images>
        <review_comments>sanitise</review_comments>
        <internal_hyperlinks>sanitise</internal_hyperlinks>
        <external_hyperlinks>sanitise</external_hyperlinks>
    </pptConfig>
    <xlsConfig>
      <macros>sanitise</macros>
        <metadata>sanitise</metadata>
        <embedded_files>sanitise</embedded_files>
        <embedded_images>sanitise</embedded_images>
        <review_comments>sanitise</review_comments>
        <internal_hyperlinks>sanitise</internal_hyperlinks>
        <external_hyperlinks>sanitise</external_hyperlinks>	
        <dynamic_data_exchange>sanitise</dynamic_data_exchange>
    </xlsConfig>
    
    <sysConfig>
        <!-- <interchange_type>xml</interchange_type> -->
        <interchange_type>sisl</interchange_type>
        <interchange_pretty>true</interchange_pretty>
        </sysConfig>
    
    <tiffConfig>
        <geotiff>sanitise</geotiff>
    </tiffConfig>
</config>



"""