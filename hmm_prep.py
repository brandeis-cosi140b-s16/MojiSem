"""
Created on Tue Apr 19 15:24:36 2016

@author: Noa Naaman

NLTK HMM trainer takes sequences of <observation, state> tuples.

The method "xml_to_tagged_tweets" takes an xml from the mojiSem gold standard
and generates a list of tagged tweets, ready for HMM training/testing

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
            ttype = tag.get('type')
            a = (n1,n2,'mm',text,ttype)
            tags.append(a)

    for tag in xml[1]:
        if tag.tag == 'content':
            spans = tag.get('spans')
            s = spans.split('~')
            n1 = int(s[0])
            n2 = int(s[1])
            text = tag.get('text')
            ttype = tag.get('type')
            a = (n1,n2,'content',text,ttype)
            tags.append(a)

    for tag in xml[1]:
        if tag.tag == 'func':
            spans = tag.get('spans')
            s = spans.split('~')
            n1 = int(s[0])
            n2 = int(s[1])
            text = tag.get('text')
            ttype = tag.get('type')
            a = (n1,n2,'func',text,ttype)
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
            ttype = tags[j][4]
            text = tags[j][3]
            tag = tags[j][2]
            #tup = (text,tag+"_"+ttype) # for subtypes
            tup = (text,tag)            # for coarse types
            i = tags[j][1]
            j = j+1
            res.append(tup)

        elif raw[i] in word_break:
            if raw[i] in ['@','#']:
                tup = (raw[i], '@#')
                res.append(tup)
                i = i + 1
            elif raw[i] in [' ', '\n']:
                tup = (raw[i], 'space')
                res.append(tup)
                i = i + 1
            else:
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
        if tup[1] == '@#':
            taggedText[i+1] = (tup[0] + taggedText[i+1][0], taggedText[i+1][1])

    taggedText = [tup for tup in taggedText if tup[1] not in ['@#','space']]
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

try:
    # Wide UCS-4 build
    has_emoji = re.compile(u'['
        u'\U0001F300-\U0001F64F'
        u'\U0001F680-\U0001F6FF'
        u'\u2600-\u26FF\u2700-\u27BF]+',
        re.UNICODE)
except re.error:
    # Narrow UCS-2 build
    has_emoji = re.compile(u'('
        u'\ud83c[\udf00-\udfff]|'
        u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
        u'[\u2600-\u26FF\u2700-\u27BF])+',
        re.UNICODE)

#emoji blocks
emoticons = re.compile(u'\ud83d[\ude00-\ude50]')
transport = re.compile(u'\ud83d[\ude80-\udec5\udecb-\uded0\udee0-\udee5\udeeb-\udeec\udee9\udef0\udef3]')
dingbats = re.compile(u'[\u2700-\u27BF]')
food = re.compile(u'\ud83c[\udf45-\udf7f\udf2d-\udf2f]')
sports = re.compile(u'\ud83c[\udfbd-\udfd3]')
animals = re.compile(u'\ud83d[\udc00-\udc3f]')
clothing = re.compile(u'\ud83d[\udc51-\udc62]')
hearts = re.compile(u'\ud83d[\udc93-\udc9f]')
office = re.compile(u'\ud83d[\udcba-\udcdc\udda5-\udddd]')
clock = re.compile(u'\ud83d[\udd50-\udd67]')
weather = re.compile(u'[\u2600-\u260D\u2614]|\ud83c[\udf21-\udf2c]')
hands = re.compile(u'[\u261A-\u261F]|\ud83d[\udc46-\udc50]|\ud83d[\udd8e-\udda3]')
plants = re.compile(u'\ud83c[\udf30-\udf44]')
celebration = re.compile(u'\ud83c[\udf80-\udf97]')

def get_emoji_group(emoji):
    if emoticons.search(emoji):
        return 'emoticon'
    elif transport.search(emoji):
        return 'transport'
    elif dingbats.search(emoji):
        return 'dingbat'
    elif food.search(emoji):
        return 'food'
    elif sports.search(emoji):
        return 'sports'
    elif animals.search(emoji):
        return 'animal'
    elif clothing.search(emoji):
        return 'clothing'
    elif hearts.search(emoji):
        return 'heart'
    elif office.search(emoji):
        return 'office'
    elif clock.search(emoji):
        return 'clock'
    elif weather.search(emoji):
        return 'weather'
    elif hands.search(emoji):
        return 'hand'
    elif plants.search(emoji):
        return 'plant'
    elif celebration.search(emoji):
        return 'celebration'
    else:
        return 'other'
    


def beg_or_end(tweet, idx):
    if idx == 0:
        return 'BEGIN'
    if idx == len(tweet) -1: #, len(tweet) - 2):
        return 'END'
    return 'MID'

def position_in_tweet(tweet, idx):
    return int(idx / float(len(tweet)) * 10)

def preceding_bipos(tags, idx):
    bi = []
    if idx > 1:
        bi.append(tags[idx - 2])
    else:
        bi.append('START')
    if idx > 0:
        bi.append(tags[idx - 1])
    else:
        bi.append('START')
    return bi

def following_bipos(tags, idx):
    bi = []
    if idx < len(tags)-1:
        bi.append(tags[idx + 1])
    else:
        bi.append('END')

    if idx < len(tags) - 2:
        bi.append(tags[idx + 2])
    else:
        bi.append('START')
    return bi

def preceded_by_determiner(tags, idx):
    return False if not idx > 0 else tags[idx-1] == 'DT'


def punctuation_follows():
    pass

def punctuation_precedes():
    pass

def enrich_observations(tweets):
    returnable = []
    for tw in tweets:
        thistweet = []
        words = [x for x,y in tw]
        tagged = nltk.pos_tag(words)
        tags = [y for x, y in tagged]
        for i in range(len(tw)):
            tok, lbl = tw[i]
            if lbl == 'func':
                lbl = 'content'
            pre = preceding_bipos(tags,i)
            post = following_bipos(tags,i)
            the_type = 'emo' if has_emoji.search(tok) else 'txt'
            emoji_group = get_emoji_group(tok) if has_emoji.search(tok) else 'txt'
            features = (  tok,
                    the_type,# is_emo?
                    tags[i], # POS


                    # position
                    position_in_tweet(tw,i),
                    beg_or_end(tw,i),
                    len(tok),

                    # contexty 
                    preceded_by_determiner(tags, i),
                    pre[1]+"|"+the_type,
                    post[0]+"|"+the_type,

                    ##'\t'.join(preceding_bipos(tags,i)), # worse
                    ##'\t'.join(following_bipos(tags,i)), # worse

                    emoji_group,

                    )
            thistweet.append((features, lbl))
        returnable.append(thistweet)
    return returnable


    #return [
            #[((
                #tok,
                #len(tok),
                #'emo' if has_emoji.search(tok) else 'txt',
                #position_in_tweet(tok, tw)
                #)
                #, lbl) for tok, lbl in tw]
            #for tw in tweets
            #]

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
