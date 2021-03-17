#!/usr/bin/env python3.8

import os
import boto3
import uuid

# CONSTANTS
AWS_REGION = os.environ['AWS_REGION']
CONNECTIONS_TABLE_NAME = os.environ['CONNECTIONS_TABLE_NAME']
AWS_SESSION = boto3.session.Session(region_name=AWS_REGION)


def lambda_handler(event, context):
    aws_params = dict(service_name='dynamodb')
    connection_id = event['requestContext']['connectionId']
    if os.environ.get('AWS_SAM_LOCAL'):
        # local dynamodb
        aws_params['endpoint_url'] = 'http://host.docker.internal:8000'
        connection_id = str(uuid.uuid4())
    dynamodb = AWS_SESSION.resource(**aws_params)
    table = dynamodb.Table(CONNECTIONS_TABLE_NAME)
    print(f'++ Connection_id: {connection_id}.')
    try:
        table.put_item(Item={'connectionId': connection_id})
    except Exception as error:
        return {'body': f'Failed to connect: {error}', 'statusCode': 500}
    return {'body': 'Connected.', 'statusCode': 200}
