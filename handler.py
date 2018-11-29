#!/usr/bin/python3
import os
import sys
import re
import json
import urllib.parse as urlparse
from botocore.vendored import requests
from boto3 import client as boto3_client

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HERE, "vendored"))

from textgenrnn import textgenrnn

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

def genText(event, context):
    textgen = textgenrnn(weights_path='model/slack_weights.hdf5',
            vocab_path='model/slack_vocab.json',
            config_path='model/slack_config.json')
    text = textgen.generate(1, max_gen_length=500, temperature=0.9, return_as_list=True)

    #punct = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~\\n\\t\'‘’“”’–—'
    #text = re.sub(' ([{}]) '.format(punct), r'\1', text[0])
    text = re.sub(' ([\':/_]) '.format(punct), r'\1', text[0])
    text = re.sub(' ([.,?!;>)\]])'.format(punct), r'\1', text)
    text = re.sub('([<@\[(]) '.format(punct), r'\1', text)
    text = re.sub('^" ', r'', text)
    text = re.sub(' "$', r'', text)
    text = re.sub('^"', r'', text)
    text = re.sub('"$', r'', text)


    data = {}
    data = {
        "response_type": "in_channel",
        "text": text
    }

    r = requests.post(event['response_url'][0], json.dumps(data))
    return r.status_code

