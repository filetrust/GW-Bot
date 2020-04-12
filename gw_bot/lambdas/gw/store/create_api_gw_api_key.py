import uuid
from gw_bot.helpers.Lambda_Helpers import log_to_elk
from osbot_aws.apis.API_Gateway import API_Gateway

def create_key_in_policy(policy_name, key_name):

    api_gateway = API_Gateway()
    usage_plan_id = api_gateway.usage_plan_id(policy_name)
    new_key       = api_gateway.api_key_create(key_name)
    key_id        = new_key.get('id')
    key_value     = new_key.get('value')
    api_gateway.usage_plan_add_key(usage_plan_id, key_id)
    return key_value

def create_key(params):
    try:

        order_id     = params.get('order_id')
        product_name = params.get('product_name')

        if product_name == 'File Type Detection - 50 (Free)':
            return create_key_in_policy('50 Free', f'50_{order_id}')
        elif product_name == 'File Type Detection - 1000 files':
            return create_key_in_policy('1k month', f'1000_{order_id}')
        elif product_name == 'File Type Detection - 50,000 files':
            return create_key_in_policy('50k month', f'50k_{order_id}')
        elif product_name == 'File Type Detection - 500,000 files':
            return create_key_in_policy('500k month', f'500k_{order_id}')
    except Exception as error:
        log_to_elk('error in create_key', f'{error}', level='error')
        return f'{error}'
    return uuid.uuid4()

def run(event, context):
    params = event.get("queryStringParameters",{})
    api_key = create_key(params)
    log_to_elk('shopify new key request create_api_gw_key', f'{params}')
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": f'{api_key}'
    }