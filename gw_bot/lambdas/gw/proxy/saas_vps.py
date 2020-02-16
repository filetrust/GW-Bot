def run(event, context):

    message =  'store saas will go here'

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": f'{message}'
    }