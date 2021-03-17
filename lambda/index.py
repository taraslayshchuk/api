#!/usr/bin/env python3.8

import random


def lambda_handler(event, context):
    return {'body': event, 'statusCode': random.choice([200, 410])}
