#!/usr/bin/python3
import json
import os
import urllib.parse as urlparse
from boto3 import client as boto3_client

lambda_client = boto3_client('lambda', region_name="eu-west-1",)

def respond(event, context):
    query = urlparse.parse_qs(event['body'])
    token = os.environ['SLACK_TOKEN']
    if (query['token'][0] != token):
        data = {
                "response_type": "ephemeral",
                "text": "Oops, seems like you are not allowed here."
                }

        objRet =  {
                'statusCode': 200,
                'body': json.dumps(data),
                }
    else:
        stage = os.environ['SERVERLESS_STAGE']
        lambda_client.invoke(
                FunctionName="jannebot-" + stage + "-gentext",
                InvocationType='Event',
                Payload=json.dumps(query)
            )
        objRet =  {
            'statusCode': 200,
        }

    return objRet

