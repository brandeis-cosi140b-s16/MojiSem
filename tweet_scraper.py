#!/usr/bin/python

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
#import pandas as pd
import matplotlib.pyplot as plt

access_token = a
access_secret = a

consumer_key = a
consumer_secret= a

class StdOutListener(StreamListener):
    def on_data(self, data):
        #print (data)
        with open('fetched_tweets2.txt','a') as tf:
            tf.write(data)
        return True
    def on_error(self, status):
        print (status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, l)

    stream.filter(track=['exams', 'finals', 'vacation', 'tree', "study", 'christmas', 'santa', 'gifts', 'shopping'])
