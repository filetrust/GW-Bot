import base64

from gw_bot.helpers.Lambda_Helpers import log_to_elk
from gw_bot.lambdas.png_to_slack import load_dependency

def log_request(path, method, headers, domain_prefix,target):
    data = { 'path': path,'method': method, 'headers':headers, 'domain_prefix':domain_prefix, 'target': target }
    log_to_elk('proxy message', data)

def run(event, context=None):
    try:
        load_dependency('requests')
        import requests
        path            = event.get('path','')
        method          = event.get('httpMethod','')
        headers         = event.get('headers',{})
        domain_prefix   = event.get('requestContext',{}).get('domainPrefix')


        request_headers = {'accept'         : headers.get('headers'        ),
                           'User-Agent'     : headers.get('User-Agent'     ),
                           'accept-encoding': headers.get('accept-encoding')}

        default_site = f'https://glasswall-file-drop.azurewebsites.net{path}'
        if   domain_prefix == 'stackoverflow' : target = f'https://stackoverflow.com{path}'
        elif domain_prefix == 'glasswall'     : target = f'https://www.glasswallsolutions.com{path}'
        elif domain_prefix == 'gw-proxy'      : target = default_site
        elif domain_prefix is not None        : target = f'https://{domain_prefix.replace("_",".")}{path}'
        else: target = f'https://glasswall-file-drop.azurewebsites.net{path}'

        log_request(path, method, headers, domain_prefix, target)

        response = requests.get(target, headers=request_headers)


        response_headers = {}

        response_body    = response.content

        for key, value in response.headers.items():           # the original value of result.headers is not serializable
            if key != 'Content-Encoding':
                response_headers[key] = str(value)

        #response_headers = {'Content-Type': 'text/html; charset=UTF-8'}


        content_type = response_headers.get('Content-Type')

        #message =  f'store saas will go here!!!: {event}'

        binary_types = [
            "application/octet-stream",
            "application/x-protobuf",
            "application/x-tar",
            "application/zip",
            "image/png",
            "image/jpeg",
            "image/jpg",
            "image/tiff",
            "image/webp",
            "image/jp2",
            'font/woff',
            'font/woff2'
        ]


        if content_type in binary_types:
            is_base_64=True
            response_body = base64.b64encode(response_body).decode("utf-8")
        else:
            is_base_64 = False
            response_body = response.text

            response_body = response_body.replace('glasswallsolutions.com', 'glasswall.gw-proxy.com')
            response_body = response_body.replace('Stack Overflow', '<b>[CHANGED BY THE PROXY]</b>')

            response_body = response_body.replace('School STEM show hits the road', 'BAE STOP with "Glasswall Inside" available in March 2020')  \
                                         .replace('We have partnered with Royal Airforce and Royal Navy to take STEM to The Belvedore Academy in Liverpool', 'Product available for pre-order at the <a href="http://glasswall-store.com/">Glasswall Store</a>') \
                                         .replace('https://www.baesystems.com/en/download-en/multimediaimage/webImage/20200214163601/1434644561633.jpg', 'https://user-images.githubusercontent.com/656739/74657297-d5f10a00-5187-11ea-908a-e9f8ca79d1fa.png') \
                                         .replace('Anger as historic car brand scrapped in Australia','BAE STOP with "Glasswall Inside" available in March 2020') \
                                         .replace('The move comes as the US car giant retreats from more markets to focus on more profitable countries.','Product available for pre-order at the <a href="http://glasswall-store.com/">Glasswall Store</a>')
                                         #.replace('https://ichef.bbci.co.uk/news/240/cpsprodpb/AFAC/production/_110927944_gettyimages-175035206.jpg', 'https://user-images.githubusercontent.com/656739/74657297-d5f10a00-5187-11ea-908a-e9f8ca79d1fa.png')


        return {
            "isBase64Encoded": is_base_64,
            "statusCode"     : 200,
            "headers"        : response_headers,
            "body"           : response_body
        }
    except Exception as error:
        message = f'Reverse Proxy error: {error}'
        log_to_elk('proxy message', message, level='error')
        return {
            "isBase64Encoded": False,
            "statusCode"     : 500,
            "headers"        : {},
            "body"           : message
        }