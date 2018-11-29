#!/usr/bin/python3
import json
import urllib.parse as urlparse
from boto3 import client as boto3_client


lambda_client = boto3_client('lambda', region_name="eu-west-1",)

def respond(event, context):
    query = urlparse.parse_qs(event['body'])
    lambda_client.invoke(
            FunctionName="jannebot-dev-gentext",
            InvocationType='Event',
            Payload=json.dumps(query)
        )
    objRet =  {
        'statusCode': 200,
    }    
    return objRet


