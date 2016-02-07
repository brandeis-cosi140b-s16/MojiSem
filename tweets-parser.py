#!/usr/bin/python
__author__ = 'hannahprovenza,orionmontoya'

import json,sys,re

def process(t):
    has_emoji = re.compile(u'['
        u'\U0001F300-\U0001F64F'
        u'\U0001F680-\U0001F6FF'
        u'\u2600-\u26FF\u2700-\u27BF]+',
    re.UNICODE)
    for line in t:
        try:
            js = json.loads(line, encoding='utf-8')
            if 'text' in js:
                if has_emoji.search(js['text']):
                    print(js['text']) # This line for rendered emoji
                    #print(line, end="") # this line for raw json
        except:
            continue

twitter = open("/Volumes/Zeitmaschin/Emoji Project/fetched_tweets2.txt", 'r', encoding='utf-8')
process(twitter)
twitter.close()
