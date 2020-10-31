import json

from osbot_aws.helpers.Lambda_Helpers import log_to_elk
from osbot_aws.Dependencies import load_dependency
from osbot_aws.apis.S3 import S3

# todo: move this to an helper class
def send_to_elk(data,id_key):
        load_dependency("elastic")
        from gw_bot.elastic.Elastic_Search import Elastic_Search
        index_id      = 'gw-cloud-trail'
        aws_secret_id = 'gw-elastic-server-1'
        elastic       = Elastic_Search(index=index_id, aws_secret_id=aws_secret_id)
        return elastic.add_bulk(data,id_key)

def run(event, context):
    try:
        records    = event.get('Records',[])
        if records:
            for record in records:
                event_name = record.get('eventName')
                region     = record.get('awsRegion')
                s3         = record.get('s3',{})
                s3_bucket  = s3.get('bucket',{}).get('name')
                s3_key     = s3.get('object', {}).get('key')
                if event_name == 'ObjectCreated:Put':
                    records_raw = S3().file_contents_from_gzip(s3_bucket, s3_key)
                    records     = json.loads(records_raw).get('Records')
                    if records:
                        result = send_to_elk(records, 'eventID')
                        log_to_elk('s3_event', f'sent {result} (of {len(records)}) CloudTrail events to elastic. After "{event_name}" event on "{region}:{s3_bucket}"')
                    #log_to_elk('on_s3_event', f'sent {result} records to Elastic')
        else:
            log_to_elk('on_s3_event', f'unsupported event: {event}')
    except Exception as error:
        return log_to_elk('error in on_s3_event', f'{error}', level='error')