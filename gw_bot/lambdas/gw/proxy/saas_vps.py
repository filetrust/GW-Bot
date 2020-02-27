import abc
import base64
from http import HTTPStatus

from gw_bot.api.proxy import Proxy, ResponseHandler
from gw_bot.helpers.Lambda_Helpers import log_error, log_to_elk
from osbot_aws.Dependencies import load_dependency


so_resp_handler = ResponseHandler(
    'Stack Overflow', '<b>[CHANGED BY THE PROXY]</b>')

pre_order = (
    'Product available for pre-order at the '
    '<a href="http://glasswall-store.com/">Glasswall Store</a>'
)
gws_resp_handler = ResponseHandler(
    [
        'glasswallsolutions.com',
        ('We have partnered with Royal Airforce and Royal Navy to '
         'take STEM to The Belvedore Academy in Liverpool'),
        ('The move comes as the US car giant retreats from '
         'more markets to focus on more profitable countries.'),
    ],
    [
        'glasswall.gw-proxy.com',
        pre_order,
        pre_order,
    ]
)


def run(event, context):
    try:
        proxy_map = {
            'stackoverflow': ['https://stackoverflow.com', so_resp_handler],
            'glasswall': [
                'https://www.glasswallsolutions.com', gws_resp_handler],
            'gw-proxy': [
                'https://glasswall-file-drop.azurewebsites.net', None],
        }
        path = event.get('path', '')
        domain_prefix = event.get(
            'requestContext', {}).get('domainPrefix', 'gw-proxy')
        item = proxy_map.get(domain_prefix)
        if item is None:
            item = [f'https://{domain_prefix.replace("_", ".")}', None]
        url = item[0]
        proxy = Proxy(f'{url}{path}')
        return proxy.handle_request(event, response_handler=item[1])
    except Exception as error:
        message = f'[gw_proxy] {error}'
        log_error('Error in Lambda', {'text': message})
        return {
            'error' : message,
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR.value,
        }
