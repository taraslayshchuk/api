#!/usr/bin/env python3.8

import os
import json
import random
import boto3
from botocore.exceptions import ClientError


# CONSTANTS
AWS_REGION = os.environ['AWS_REGION']
WORDS_TABLE_NAME = os.environ['WORDS_TABLE_NAME']
CONNECTIONS_TABLE_NAME = os.environ['CONNECTIONS_TABLE_NAME']
AWS_SESSION = boto3.session.Session(region_name=AWS_REGION)


def _get_random_word_from_table(dynamodb):
    """
    Retrieve a random word from Dynamo DB.
    """
    table = dynamodb.Table(WORDS_TABLE_NAME)
    # item_count = table.item_count
    item_count = table.scan(Select='COUNT').get('Count')
    random_id = random.randint(1, item_count)
    item = table.get_item(Key={'id': random_id})
    return item.get('Item').get('word')


def _send_to_connection(connection_id, data, dynamodb, gatewayapi):
    """
    Send data to open websocket connection.
    """

    try:
        print(f'++ Sending data {data} to connection {connection_id}.')
        gatewayapi.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode('utf-8'))
    except ClientError as error:
        if error.response['ResponseMetadata']['HTTPStatusCode'] == 410:
            print(f'!! Found stale connection, deleting {connection_id}.')
            table = dynamodb.Table(CONNECTIONS_TABLE_NAME)
            table.delete_item(Key={'connectionId': connection_id})
    except Exception as error:
        print(f'!! {error}.')


def lambda_handler(event, context):
    aws_db_params = dict(service_name='dynamodb')
    aws_api_params = dict(service_name='apigatewaymanagementapi',
                          endpoint_url=f'https://{event["requestContext"]["domainName"]}/{event["requestContext"]["stage"]}'
                          )
    if os.environ.get('AWS_SAM_LOCAL'):
        # local dynamodb
        aws_db_params['endpoint_url'] = 'http://host.docker.internal:8000'
        # local fake api gateway
        aws_api_params['endpoint_url'] = f'http://{event["requestContext"]["domainName"]}/{event["requestContext"]["stage"]}'
    gatewayapi = AWS_SESSION.client(**aws_api_params)
    dynamodb = AWS_SESSION.resource(**aws_db_params)

    # Getting all current connections
    table = dynamodb.Table(CONNECTIONS_TABLE_NAME)
    connection_data = []
    try:
        connection_data = table.scan(ProjectionExpression='connectionId').get('Items', [])
    except Exception as error:
        return {'body': str(error), 'statusCode': 500}
    connections = [i['connectionId'] for i in connection_data if 'connectionId' in i]
    print(f'++ Found {len(connections)} connections.')

    # Getting a random word
    word = _get_random_word_from_table(dynamodb)

    # Sending data to all connections
    data = {'word': word}
    for connection in connections:
        _send_to_connection(connection, data, dynamodb, gatewayapi)
    return {'body': 'Data sent.', 'statusCode': 200}
