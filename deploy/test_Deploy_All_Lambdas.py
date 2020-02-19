
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper


class test_Deploy_All_Lambdas(Test_Helper):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_deploy_all_lambdas(self):
        lambdas_to_deploy = {'deploy_lambda__browser' : ['osbot_browser.lambdas.aws_web'        ,
                                                         'osbot_browser.lambdas.jira_web'       ,
                                                         'osbot_browser.lambdas.lambda_browser' ,
                                                         'osbot_browser.lambdas.google_chart'   ,
                                                         'osbot_browser.lambdas.slack_web'      ,
                                                         'osbot_browser.lambdas.gw.sow'         ,
                                                         'osbot_browser.lambdas.gw.xml_report' ],
                             'deploy_lambda__jira'    : ['osbot_jira.lambdas.elastic_jira'      ,
                                                         'osbot_jira.lambdas.elk_to_slack'      ,
                                                         'osbot_jira.lambdas.graph'             ,
                                                         'osbot_jira.lambdas.jira'              ,
                                                         'osbot_jira.lambdas.on_jira_change'    ,
                                                         'osbot_jira.lambdas.slack_actions'     ,
                                                         'osbot_jira.lambdas.slack_jira_actions',
                                                         'osbot_jira.lambdas.gw.gw_jira'       ],
                             'deploy_lambda__jupyter' : ['osbot_jupyter.lambdas.browser'        ,
                                                         'osbot_jupyter.lambdas.execute_python' ,
                                                         'osbot_jupyter.lambdas.jupyter_web'    ,
                                                         'osbot_jupyter.lambdas.nbconvert'      ,
                                                         'osbot_jupyter.lambdas.osbot'          ,
                                                         'osbot_jupyter.lambdas.screenshot'     ,
                                                         'osbot_jupyter.lambdas.start_server']  ,
                             'deploy_lambda__gw_bot'  : ['gw_bot.lambdas.gw_bot'                ,
                                                         'gw_bot.lambdas.log_to_elk'            ,
                                                         'gw_bot.lambdas.png_to_slack'          ,
                                                         'gw_bot.lambdas.puml_to_png'           ,
                                                         'gw_bot.lambdas.puml_to_slack'         ,
                                                         'gw_bot.lambdas.slack_message'         ,
                                                         'gw_bot.lambdas.slack_callback'        ,
                                                         'gw_bot.lambdas.aws.commands'          ,
                                                         'gw_bot.lambdas.aws.on_s3_event'       ,
                                                         'gw_bot.lambdas.gw.commands'           ,
                                                         'gw_bot.lambdas.gw.gw_engine'          ,
                                                         'gw_bot.lambdas.gw.gw_report'          ,
                                                         'gw_bot.lambdas.gw.gw_slack_file'      ,
                                                         'gw_bot.lambdas.gw.libreoffice'        ,
                                                         'gw_bot.lambdas.gw.proxy.on_firehose_record',
                                                         'gw_bot.lambdas.gw.proxy.saas_vps'     ,
                                                         'gw_bot.lambdas.gw.store.commands'     ,
                                                         'gw_bot.lambdas.gw.store.create_api_gw_api_key']}

        deploy = Deploy()
        deployed = []
        for method_name, lambdas_names in lambdas_to_deploy.items():
            for lambda_name in lambdas_names:
                getattr(deploy,method_name)(lambda_name)
                deployed.append(lambda_name)

        self.result =  deployed
