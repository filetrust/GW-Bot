#rm -rf tmp-output;
# #docker run --rm -v /tmp/tmp-input:/home/classic_cli/input -v /tmp/tmp-output/:/home/classic_cli/output -v /tmp/tmp-config:/home/classic_cli/config safiankhan/glasswallclassic:2.0
# ./glasswallCLI -config=./config/config.ini -xmlconfig=./config/config.xml ;
#
# cat tmp-output/glasswallCLIProcess.log
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

    def docker_cli(self, command):
        params = ['run', '--rm',
                         '-v', self.tmp_input  + ':/home/classic_cli/input' ,
                         '-v', self.tmp_output + ':/home/classic_cli/output',
                         '-v', self.tmp_config + ':/home/classic_cli/config',
                         self.docker_image                                  ,
                        './glasswallCLI'
                  ]
        params.extend(command)
        return self.docker_exec(params)

    def docker_scan(self):
        command = ['-config=./config/config.ini', '-xmlconfig=./config/config.xml']
        return self.docker_cli(command)
