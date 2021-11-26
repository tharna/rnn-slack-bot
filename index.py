#!/usr/bin/python3
from slack_sdk import WebClient
import json
import os
from urllib.parse import parse_qs
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
def respond(event, context):
    params = parse_qs(event['body'])
    
    print(params)

    objRet =  {
        'statusCode': 200
    }

    #APP token (Bot User OAuth Access Token) Can be found in Created APP > OAuth & Permissions
    result = client.chat_postMessage(
        channel=params['channel_id'][0],
        text=params['text'][0]
    )

    return objRet

