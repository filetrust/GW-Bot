from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.api.gw.sdk_1_x.API_Glasswall_Docker import API_Docker_Glasswall


class test_API_Docker_Glasswall_1_x(TestCase):
    def setUp(self) -> None:
        self.glasswall = API_Docker_Glasswall()
        self.result    = None

    def tearDown(self) -> None:
        if self.result is not None:
            Dev.pprint(self.result)

    def test_ctor(self):
        assert self.glasswall.docker_image == 'safiankhan/glasswallclassic:2.0'

    def test_docker_cli(self):
        #assert self.glasswall.docker_cli(['-v']) == '1.42.33256\nSUCCESS\n'
        self.result =self.glasswall.docker_cli(['ls','config'])


    def test_docker_scan(self):
        self.result = self.glasswall.docker_scan()

    def test_docker_run_bash_command(self):
        assert 'home'                      in self.glasswall.docker_run_bash_command(['ls','/'])
        assert 'glasswallCLI'              in self.glasswall.docker_run_bash_command(['ls'])
        assert 'executable file not found' in self.glasswall.docker_run_bash_command('aaaa')
