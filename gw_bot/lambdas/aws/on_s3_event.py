import json

from gw_bot.helpers.Lambda_Helpers import log_to_elk
from gw_bot.lambdas.png_to_slack import load_dependency
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
        for record in records:
            event_name = record.get('eventName')
            region     = record.get('awsRegion')
            s3         = record.get('s3',{})
            s3_bucket  = s3.get('bucket',{}).get('name')
            s3_key     = s3.get('object', {}).get('key')
            if event_name == 'ObjectCreated:Put':
                records_raw = S3().file_contents_from_gzip(s3_bucket, s3_key)
                records     = json.loads(records_raw).get('Records')
                log_to_elk('on_s3_event', f'After "{event_name}" event on bucket "{s3_bucket}" on region "{region}", sending "{len(records)}" entries to elastic')
                result = send_to_elk(records, 'eventID')
                log_to_elk('on_s3_event', f'sent {result} records to Elastic')
    except Exception as error:
        return log_to_elk('error in on_s3_event', f'{error}', level='error')