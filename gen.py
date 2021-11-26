#!/usr/bin/python3
import os
import sys
import re
import RAKE

from textgenrnn import textgenrnn
#sys.stdout = os.devnull
#sys.stderr = os.devnull

Rake = RAKE.Rake(RAKE.SmartStopList())
topic = ""

if len(sys.argv) > 1:
    topic = Rake.run(sys.argv[1])
    print(sys.argv[1])
    print(topic)

if topic:
    print(topic[0][0])
    prefix = topic[0][0]
else:
    prefix = ""


textgen = textgenrnn(weights_path='model/slack_weights.hdf5',
                       vocab_path='model/slack_vocab.json',
                       config_path='model/slack_config.json')
text = textgen.generate(n=1, prefix=prefix, max_gen_length=500, temperature=0.6, return_as_list=True)
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

print(prefix)
punct = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~\\n\\t\'‘’“”’–—'
##text = re.sub(' ([{}]) '.format(punct), r'\1', text[0])
text = re.sub(' ([\':/_]) '.format(punct), r'\1', text[0])
#text = re.sub(' ([.,?!;>)\]])'.format(punct), r'\1', text)
#text = re.sub('([<@\[(]) '.format(punct), r'\1', text)
text = re.sub('^"', r'', text)
text = re.sub('"$', r'', text)

print(text)
