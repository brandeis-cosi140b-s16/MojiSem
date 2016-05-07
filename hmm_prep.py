"""
Created on Tue Apr 19 15:24:36 2016

@author: Noa Naaman

NLTK HMM trainer takes sequences of <observation, state> tuples.

The method "xml_to_tagged_tweets" takes an xml from the mojiSem gold standard and generates a list of tagged tweets, ready for HMM training/testing

"""

import re
import nltk
from xml.etree.ElementTree import ElementTree

def process_gold(path):
    #f = nltk.data.find(path)
    f = open(path)
    xml = ElementTree().parse(f)
    tags = []

    for tag in xml[1]:
        if tag.tag == 'mm':
            spans = tag.get('spans')
            s = spans.split('~')
            n1 = int(s[0])
            n2 = int(s[1])
            text = tag.get('text')
            a = (n1,n2,'mm',text)
            tags.append(a)

    for tag in xml[1]:
        if tag.tag == 'content':
            spans = tag.get('spans')
            s = spans.split('~')
            n1 = int(s[0])
            n2 = int(s[1])
            text = tag.get('text')
            a = (n1,n2,'content',text)
            tags.append(a)

    for tag in xml[1]:
        if tag.tag == 'func':
            spans = tag.get('spans')
            s = spans.split('~')
            n1 = int(s[0])
            n2 = int(s[1])
            text = tag.get('text')
            a = (n1,n2,'func',text)
            tags.append(a)

    tags = sorted(tags)

    raw = xml[0].text
    return raw, tags

    
def tag_text(raw, tags):

    i = 0
    j = 0
    res = []
    tweet_id = re.compile(r'[0-9]{18}')
    word_break = [' ', '\n', '!', '.', '?', ':', ';', ',', '#', '@']
    
    while i < len(raw):

        if j >= len(tags):
            j = 0
        if i == tags[j][0]:
            text = tags[j][3]
            tag = tags[j][2]
            tup = (text,tag)
            i = tags[j][1]
            j = j+1
            res.append(tup)

        elif raw[i] in word_break:
            tup = (raw[i], 'punc')
            res.append(tup)
            i = i + 1


        else:
            text = ''
            while (i < len(raw)) and (raw[i] not in word_break) and (i != tags[j][0]):
                text = text + raw[i]
                i = i + 1
            if tweet_id.search(text):
                tup = (text, 'new_tweet')
                res.append(tup)
            else:
                tup = (text, 'word')
                res.append(tup)

    return res

def attach_punc(taggedText):
    for i in range(len(taggedText)):
        tup = taggedText[i]
        if tup[1] == 'punc':
            if tup[0] in ['#','@']:
                taggedText[i+1] = (tup[0] + taggedText[i+1][0], taggedText[i+1][1])

            if tup[0] in ['!', '.', '?', ':', ';', ',']:
                taggedText[i-1] = (taggedText[i-1][0] + tup[0], taggedText[i-1][1])

    taggedText = [tup for tup in taggedText if tup[1] != 'punc']
    return taggedText

def split_to_tweets(taggedText):
    tagged_tweets = []
    i = 0
    while i < len(taggedText):
        if taggedText[i][1] == 'new_tweet':
            j = i
            i = i + 1
            while i < len(taggedText) and (taggedText[i][1] != 'new_tweet'):
                i = i + 1
            tweet = taggedText[j:i]
            tagged_tweets.append(tweet)

    for i in range(len(tagged_tweets)):
        tagged_tweets[i] = [tup for tup in tagged_tweets[i] if tup[1] != 'new_tweet']

    return tagged_tweets

has_emoji = re.compile(u'['
    u'\U0001F300-\U0001F64F'
    u'\U0001F680-\U0001F6FF'
    u'\u2600-\u26FF\u2700-\u27BF]+',
re.UNICODE)

def enrich_observations(tweets):
    return [[((tok, len(tok), 'emo' if has_emoji.search(tok) else 'txt'), lbl) for tok, lbl in tw] for tw in tweets]

def split_dataset(dataset, testset_percentage):
    cutoff = int(testset_percentage * len(dataset) / 100)
    return dataset[cutoff:], dataset[:cutoff]

def xml_to_tagged_tweets(path):
    raw, tags = process_gold(path)
    taggedText = tag_text(raw, tags)
    taggedText = attach_punc(taggedText)
    tweets = split_to_tweets(taggedText)
    tweets = enrich_observations(tweets)
    return tweets
