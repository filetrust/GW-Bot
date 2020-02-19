import  unittest

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.lambdas.puml_to_slack import run


class Test_puml_to_slack(Test_Helper):
    def setUp(self):
        super().setUp()
        self.puml_to_slack = Lambda('gw_bot.lambdas.puml_to_slack')

    def test_update_lambda(self):
        self.result = Deploy().setup().deploy_lambda_puml_to_slack()

    def test_invoke_directly(self):
        puml = "@startuml \n aaa30->bbb12 \n @enduml"
        self.result = run({"puml": puml, 'channel': 'DRE51D4EM'},None)

    def test_update_invoke(self):
        #self.test_update_lambda()
        puml = "@startuml \n aaa30->bbb12 \n @enduml"
        self.result = self.puml_to_slack.invoke({"puml": puml,'channel': 'DRE51D4EM'})

        Dev.pprint(self.result)
        #from pbx_gs_python_utils.utils.Show_Img import Show_Img
        #Show_Img.from_svg_string(result['png_base64'])

    def test_just_invoke___more_complex_diagram(self):

        puml = """
@startuml
/'skinparam dpi 500 '/
:Main aaa Admin: as Admin
(Use the application) as (Use)

User -> (Start)
User --> (Use)
(Use) --> (b50011)

Admin ---> (Use)

note right of admin : This is an example.

note right of (Use)
  A note can also
  be on several lines
  very cool
end note

note "This note is connected\\nto several objects." as N2
(Start) .. N2
N2 .. (Use)
@enduml
"""
        result = self.plant_to_png.invoke({"puml": puml})
        from pbx_gs_python_utils.utils.Show_Img import Show_Img
        Show_Img.from_svg_string(result['png_base64'])