#!/usr/bin/python3
import os
import sys
import re

from textgenrnn import textgenrnn
sys.stdout = os.devnull
sys.stderr = os.devnull
textgen = textgenrnn(weights_path='model/slack_weights.hdf5',
                       vocab_path='model/slack_vocab.json',
                       config_path='model/slack_config.json')
text = textgen.generate(1, max_gen_length=500, temperature=0.9, return_as_list=True)
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

punct = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~\\n\\t\'‘’“”’–—'
#text = re.sub(' ([{}]) '.format(punct), r'\1', text[0])
text = re.sub(' ([\':/_]) '.format(punct), r'\1', text[0])
text = re.sub(' ([.,?!;>)\]])'.format(punct), r'\1', text)
text = re.sub('([<@\[(]) '.format(punct), r'\1', text)
text = re.sub('^" ', r'', text)
text = re.sub(' "$', r'', text)

print(text)
