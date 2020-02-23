def run(event, context):
    message =  "Hello {0} (from lambda)".format(event.get('name'))
    #message = f'{event.get("queryStringParameters")}'
    #return message
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": f'{message}'
    }