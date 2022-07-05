#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# os.chdir('/home/localadmin/Documents/Spartan/')
import os
import pandas as pd
import re, spacy
import numpy as np

import sys
#import importlib
#importlib.reload(sys)
#reload(sys)
#sys.setdefaultencoding("utf-8")

nlp = spacy.load('en_core_web_lg')#lg
#from sklearn.feature_extraction.text import CountVectorizer
from spacy.lang.en.stop_words import STOP_WORDS
from timeit import default_timer as timer


STOP_WORDS.update(['%', 'em', "<", ">", "β", "à", "×", '+', '@'])

print('Spacy and libraries successfully loaded!')

# We define the function here

nlp.max_length=4000000

def normalize_string(text, nlp, STOP_WORDS, lemmatize=True, tokenize=True, stopwords = True,
                     punct = True, regex = None, remove_pronoun = True, fix_stops = True):
    # Use spacy to tokenize + do POS tagging + lemmas and such
    text = nlp(text)


    if punct:
        # We get rid of punctuation, symbols (=, +) and PART, things like 's'
        text = [token for token in text if not token.pos_ in ['PUNCT', 'SYM', 'PART', 'SPACE', 'NUM']]

    if lemmatize:
        text = [token.lemma_ for token in text]

        if remove_pronoun:
            text = [x for x in text if not (x == "-PRON-")]

        if stopwords:
            # Changed this to use branching logic for more efficiency.
            text = [token for token in text if not token in STOP_WORDS]

    else:
        text = [token.text.lower() for token in text]
        if stopwords:
            text = [token for token in text if not token in STOP_WORDS]

    # Remove custom patterns. Allows for a list of patterns, or just one,
    # though I'm certain there's a more elegant way to do this. We do this
    # after lemmatizing so we can work on text more efficiently.

    if regex is not None:
        # Turn a single item into a list of 1
        if not isinstance(regex, list):
            regex = [regex]
        # Iterate through the list of regex and remove matching tokens.
        # Have used filter and compiled regex to attempt speedups.
        # as at https://stackoverflow.com/questions/3640359/regular-expressions-search-in-list
        # Since python doesn't automatically vectorise grep statements like R does.
        for i in range(len(regex)):

            # Note: this line assumes you're passing a list of compiled regex
            # to create increased efficiencies.
            # r = re.compile(regex[i])
            text = list(filter(lambda x: not regex[i].match(x), text))

    # After the regex filters, we remove dashes from before or after words so they'll match more easily, because they don't mean different things here.
    # Same with full stops before words. Minor, but it's more correct.
    if fix_stops:
        text = [re.sub(r'(\w)\-+$', '\\1', token) for token in text]
        text = [re.sub(r'^-+(\w)', '\\1', token) for token in text]
        text = [re.sub(r'^\.+(\w)', '\\1', token) for token in text]

    # We undo spacy's inherent tokenizing if told to do so.
    if not tokenize:
        text = ' '.join([token for token in text])




    return text

mylist = []
import sys,codecs

# Running the tokenizer straight over the data to basically just create abstracts that have been cleaned up a bit, with
writer = codecs.open(sys.argv[1]+".processed.all",'w', encoding='utf-8')
reader = codecs.open(sys.argv[1],'r', encoding = 'utf-8')
#_id=0
with codecs.open(sys.argv[1],'r') as _file:##raw (abstract,year) data
#	writer.write(_file.readline())##header
	for line in _file.readlines():
		if len(re.split(r' \|\|\|\|\| ', line))>2:
			#_id+=1
			abstract, year, journal_old, journal_new = re.split(r' \|\|\|\|\| ', line) 
			#abstract, year, journal_old = re.split(r' \|\|\|\|\| ', line)
			abstract_new = normalize_string(abstract, nlp = nlp, lemmatize=True, STOP_WORDS = STOP_WORDS, punct=True, tokenize=True)
	
			writer.write(' '.join(abstract_new)+" ||||| " +year+" ||||| "+journal_old+" ||||| "+journal_new)
			#writer.write(' '.join(abstract_new)+" ||||| "+unicode(abstract)+" ||||| " +year+" ||||| "+unicode(journal_old))
writer.close()
























#
