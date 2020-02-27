import base64
from http import HTTPStatus

from gw_bot.helpers.Lambda_Helpers import log_to_elk
from osbot_aws.Dependencies import load_dependency


BINARY_CONTENT_TYPES = [
    'application/octet-stream',
    'application/x-protobuf',
    'application/x-tar',
    'application/zip',
    'image/png',
    'image/jpeg',
    'image/jpg',
    'image/tiff',
    'image/webp',
    'image/jp2',
    'font/woff',
    'font/woff2',
]


class Proxy():

    def __init__(self, url):
        self.url = url

    def log_request(self, path, method, headers, domain_prefix, target):
        data = {
            'path': path,
            'method': method,
            'headers': headers,
            'domain_prefix': domain_prefix,
            'target': target,
        }
        log_to_elk('proxy message', data)

    def is_binary_content_type(self, response):
        return response.headers.get('Content-Type') in BINARY_CONTENT_TYPES

    def get_response_body(self, response):
        if self.is_binary_content_type(response):
            response_body = base64.b64encode(response.content).decode('utf-8')
        else:
            response_body = response.text
        return response_body

    def proxy_request(self, request_headers):
        return requests.get(self.url, headers=request_headers)

    def response(self, is_base_64, status, headers, body):
        return {
            'isBase64Encoded': is_base_64,
            'statusCode': status,
            'headers': headers,
            'body': body,
        }

    def handle_request(self, event, response_handler=None):
        load_dependency('requests')
        import requests
        path = event.get('path', '')
        method = event.get('httpMethod', '')
        headers = event.get('headers', {})
        domain_prefix = event.get('requestContext', {}).get('domainPrefix')
        try:
            self.log_request(path, method, headers, domain_prefix, self.url)

            request_headers = {
                'accept': headers.get('headers'),
                'User-Agent': headers.get('User-Agent'),
                'accept-encoding': headers.get('accept-encoding'),
            }
            response = requests.get(self.url, headers=request_headers)

            # The original value of result.headers is not serializable:
            response_headers = {}
            for key, value in response.headers.items():
                if key != 'Content-Encoding':
                    response_headers[key] = str(value)

            response_body = self.get_response_body(response)
            if response_handler:
                response_body = response_handler.process(response_body)
            return self.response(
                self.is_binary_content_type(response), HTTPStatus.OK.value,
                response_headers, response_body
            )
        except Exception as error:
            message = f'Proxy error: {error}'
            log_to_elk('proxy message', message, level='error')
            return self.response(
                False, HTTPStatus.INTERNAL_SERVER_ERROR.value, headers, message
            )


class ResponseHandler():

    def __init__(self, search, replace):
        """
        Initiate a handler with `search` and `replace`. They both should
        be of type either string or list. In the case of strings the
        `search` is searched in a response and replaced by
        `replace`. In the case of list each element from `search` is
        searched in a response and replaced by an appropriate element
        from `replace`.
        """
        self.search = [search] if isinstance(search, str) else search
        self.replace = [replace] if isinstance(search, str) else replace
        if len(self.search) != len(self.replace):
            raise ValueError('Lenghts of `search` and `replace` are not equal')

    def process(self, response):
        for i, s in enumerate(self.search):
            response = response.replace(s, self.replace[i])
        return response
