from gw_bot.elastic.Log_To_Elk import Log_To_Elk
from osbot_aws.helpers.Test_Helper import Test_Helper


class Test_Log_To_Elk(Test_Helper):

    def setUp(self):
        super().setUp()
        self.log_to_elk = Log_To_Elk()
        self.result     = None

    def test_setup(self):
        assert self.log_to_elk.elastic.index    == 'elastic_logs'
        assert self.log_to_elk.elastic.port     == '9243'
        assert self.log_to_elk.elastic.username == 'elastic'

    def test_log_debug(self):
        response = self.log_to_elk.log_debug('this is a debug message from a unit test')
        assert response.get('elastic_response').get('result') == 'created'

    def test_log_info(self):
        response = self.log_to_elk.log_info('this is a debug message from a unit test')
        assert response.get('elastic_response').get('result') == 'created'

    def test_log_error(self):
        response = self.log_to_elk.log_error('this is a debug message from a unit test')
        assert response.get('elastic_response').get('result') == 'created'