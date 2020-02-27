from http import HTTPStatus
from unittest import mock

from pbx_gs_python_utils.utils.Http import GET

from gw_bot.helpers.Test_Helper import Test_Helper
from gw_bot.api.proxy import Proxy, ResponseHandler
from osbot_aws.apis.API_Gateway import API_Gateway
from osbot_aws.helpers.Rest_API import Rest_API


class test_response_handler(Test_Helper):

    def test_strings(self):
        search = 'foo'
        replace = 'bar'
        handler = ResponseHandler(search, replace)

        response = handler.process('foobarbaz')

        assert response == 'barbarbaz'

    def test_lists(self):
        search = ['foo']
        replace = ['bar']
        handler = ResponseHandler(search, replace)

        response = handler.process('foobarbaz')

        assert response == 'barbarbaz'

    def test_lists_multiple_items(self):
        search = ['foo', 'baz']
        replace = ['bar', 'jaz']
        handler = ResponseHandler(search, replace)

        response = handler.process('foobarbaz')

        assert response == 'barbarjaz'

    def test_unequal_lists(self):
        search = ['foo', 'baz']
        replace = ['bar']
        try:
            handler = ResponseHandler(search, replace)
        except ValueError as error:
            msg = 'Lenghts of `search` and `replace` are not equal'
            assert error.args[0] == msg


class test_proxy(Test_Helper):

    def setUp(self):
        self.proxy = Proxy('http://example.com')
        self.result = None
        self.png_data = None

    @mock.patch('requests.get')
    def test_handle_response(self, mockget):
        headers = {
            'Content-Type': 'text',
        }
        attrs = {'headers.return_value': headers}
        response = mock.Mock(**attrs)
        response.headers = headers
        # response.content = b'test content'
        response.text = b'test content'
        mockget.return_value = response

        resp = self.proxy.handle_request({})

        assert resp['isBase64Encoded'] == False
        assert resp['statusCode'] == HTTPStatus.OK.value
        assert resp['headers']['Content-Type'] ==  'text'
        assert b'test content' in resp['body']

    @mock.patch('requests.get')
    def test_handle_binary_response(self, mockget):
        headers = {
            'Content-Type': 'image/png',
        }
        attrs = {'headers.return_value': headers}
        response = mock.Mock(**attrs)
        response.headers = headers
        response.content = b'test content'
        mockget.return_value = response

        resp = self.proxy.handle_request({'headers': headers})

        assert resp['isBase64Encoded'] == True
        assert resp['statusCode'] == HTTPStatus.OK.value
        assert resp['headers']['Content-Type'] ==  'image/png'

    @mock.patch('requests.get')
    def test_internal_server_error(self, mockget):
        mockget.side_effect = Exception('proxy error')

        resp = self.proxy.handle_request({})

        assert resp['isBase64Encoded'] == False
        assert resp['statusCode'] == HTTPStatus.INTERNAL_SERVER_ERROR.value
        assert resp['body'] == 'Proxy error: proxy error'

    @mock.patch('requests.get')
    def test_log_request(self, mockget):
        headers = {
            'Content-Type': 'text/html; charset=UTF-8',
        }
        self.proxy.log_request = mock.Mock()

        resp = self.proxy.handle_request({
            'path': '/path',
            'httpMethod': 'GET',
            'headers': headers,
            'requestContext': {
                'domainPrefix': 'prefix',
            },
        })

        self.proxy.log_request.assert_called_once_with(
            '/path', 'GET', headers, 'prefix', 'http://example.com')
