from gw_bot.helpers.Lambda_Helpers import log_to_elk


def run(event, context=None):
    log_to_elk('on-firehose-record', f'{event}')
    return 'on_firehose_record'

