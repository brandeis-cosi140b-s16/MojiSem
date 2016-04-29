#!/usr/bin/python
__author__ = 'hannahprovenza,orionmontoya'

import json,sys,re

def process(t):
    stripped_bodies = {}
    has_emoji = re.compile(u'['
        u'\U0001F300-\U0001F64F'
        u'\U0001F680-\U0001F6FF'
        u'\u2600-\u26FF\u2700-\u27BF]+',
    re.UNICODE)
    for line in t:
        try:
            js = json.loads(line, encoding='utf-8')
            if 'text' in js:
                if 'http' in js['text'] or 'www.' in js['text']:
                    continue
                elif (js['lang'] != 'en'):
                    continue
                elif has_emoji.search(js['text']):
                    stripped_bodies[strip_varying(js['text'])] = js
        except:
            continue
    for js in stripped_bodies.values():
        print(js['id'],js['text']) # This line for rendered emoji
        #print(line, end="") # this line for raw json

def strip_varying(text):
    text = re.sub('#\w* ','',text)
    text = re.sub('@\w* ','',text)
    return text
    #text = re.sub('@\w* ','',text)


#twitter = open("/Volumes/Zeitmaschin/Emoji Project/fetched_tweets2.txt", 'r', encoding='utf-8')
twitter = open("shorttweets3-4.txt", 'r', encoding='utf-8')
process(twitter)
twitter.close()


"""
698362173567868928
698495729212461057
698495880308064257 https://t.co/rJYuo2AzwB
698495900440723456
698504727336607744
698504785490800644
698504801185832960
698504807192068097
698504810748841986 <- non-communicative:artistic
698504861692743680
698504862837952512 <- what is the missing word?
698504884581175297 <- "epcot bound"
698504973227814912 <- fascinating to see that spam tweets are nevertheless useful linguistic data in this study
698504983847821312 <- unclear connection to content
698505041448034304 what does dark moonface mean??? even I use it but I don't know what it means
698505052529561600 MUA = make-up artist?
698505058204385280
698505061979201536
698505286567350272 <- you know, some of the predicate uses seem performative to me, not exactly linguistic
698506941161549824
698506982924423172 <- contrast with the one where the emoji are all relevant -- these are generic or something
698506984006492160 "miss you all (sending you love) can't wait to see you all (it'll be a blast!)"
698506995591151618 (french)
698507007175888896 (emoji+image, nothing more)
698507018475323392 ear buds, music notes suggest song lyrics
698507360877289472 haha yes, guitar means Slash :)
698507028302471168 <- I love how they compose "fast wifi"
698507072162394112 football topic
698507074720952320 teacup+leaves = happiness
698507087429689344 there are flag emoji but they use shamrock metonymically
698507166945304577 both redundant (to the moon) and emotive (heart-eyes)
698507168237142016 huge semantic load in the emoji (Tulum, Mexico)
698507183382798336 (long tweet: possibly a space-saver)
698507183588245504 this is just great (DNA)
698507194577379328 this is using an x as a kiss despite also using emoji???

desperately need deduplication

propagation of memes/snowclones/emoji as line-final list-element markers



do the framed-image emoji co-occur with image links, as if giving readers a preview of what the link holds?

twitter users also have extrinsic constraint on character count; this can lead to opportunistic replacements to shorten messages as well --
a fascinating adaptation to message limitations, and a novel source of need-motivated language change




"""
