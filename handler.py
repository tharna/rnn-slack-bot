#!/usr/bin/python3
import os
import sys
import re
import json
from urllib.parse import urlencode
from botocore.vendored import requests

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HERE, "vendored"))

import RAKE
from textgenrnn import textgenrnn

def genText(event, context):
    question = event['event']['text']
    if len(question) > 0:
        Rake = RAKE.Rake(RAKE.SmartStopList())
        question = re.sub('<@UFWT0DGNA>', r'', question)
        topic = Rake.run(question)

    if topic:
        prefix = topic[0][0]
    else:
        prefix = ""

    textgen = textgenrnn(weights_path='model/slack_weights.hdf5',
            vocab_path='model/slack_vocab.json',
            config_path='model/slack_config.json')
    text = textgen.generate(n=1, prefix=prefix, max_gen_length=500, temperature=0.8, return_as_list=True)

    punct = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~\\n\\t\'‘’“”’–—'
    ##text = re.sub(' ([{}]) '.format(punct), r'\1', text[0])
    text = re.sub(' ([\':/_]) '.format(punct), r'\1', text[0])
    #text = re.sub(' ([.,?!;>)\]])'.format(punct), r'\1', text)
    #text = re.sub('([<@\[(]) '.format(punct), r'\1', text)
    #text = re.sub('^" ', r'', text)
    #text = re.sub(' "$', r'', text)
    text = re.sub('^"', r'', text)
    text = re.sub('"$', r'', text)

    data = {}
    data = {
        "channel": event['event']['channel'],
        "text": text
    }

    #APP token (Bot User OAuth Access Token) Can be found in Created APP > OAuth & Permissions
    token = os.environ['BOT_TOKEN']

    r = requests.post("https://slack.com/api/chat.postMessage?token="+token+"&as_user=true&channel=" + event['event']['channel'] + "&text=" + text)
    return r.status_code

    #data = {}
    #data = {
    #    "response_type": "in_channel",
    #    "text": text
    #}

    #r = requests.post(event['response_url'][0], json.dumps(data))
    #return r.status_code

