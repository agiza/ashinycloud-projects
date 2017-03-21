# -*- coding: utf-8 -*-

import json
import boto3


def handler(event, context):
    print 'Event:', event
    lambda_client = boto3.client('lambda')
    if 'config_bucket' not in event:
        raise Exception('Missing config_bucket')
    if 'lambda_function' not in event:
        raise Exception('Missing lambda_function')

    bucket = boto3.resource('s3').Bucket(event['config_bucket'])
    result = bucket.meta.client.list_objects(
        Bucket=bucket.name, Prefix='/', Delimiter='/'
    )
    for dataset_prefixes in result.get('CommonPrefixes'):
        event['dataset_prefix'] = dataset_prefixes
        response = lambda_client.invoke(
            FunctionName=event['lambda_function'],
            InvocationType='Event',
            Payload=json.dumps(event)
        )
        print response
