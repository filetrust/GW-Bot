import base64

from gw_bot.helpers.Lambda_Helpers import log_to_elk
from gw_bot.lambdas.png_to_slack import load_dependency

def log_request(path, method, headers):
    data = { 'path': path,'method': method, 'headers':headers }
    log_to_elk('proxy message', data)

def run(event, context=None):
    load_dependency('requests')
    import requests
    path            = event.get('path','')
    method          = event.get('httpMethod','')
    headers         = event.get('headers',{})
    log_request(path, method,headers)
    request_headers = {'accept'         : headers.get('headers'        ),
                       'User-Agent'     : headers.get('User-Agent'     ),
                       'accept-encoding': headers.get('accept-encoding')}

    target = f'https://glasswall-file-drop.azurewebsites.net{path}'
    response = requests.get(target,headers=request_headers)
    response_headers = {}

    response_body    = response.content

    for key, value in response.headers.items():           # the original value of result.headers is not serializable
        response_headers[key] = str(value)

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
    return {
        "isBase64Encoded": is_base_64,
        "statusCode"     : 200,
        "headers"        : response_headers,
        "body"           : response_body
    }