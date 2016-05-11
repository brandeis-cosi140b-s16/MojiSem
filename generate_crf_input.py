# -*- coding: utf-8 -*-
import sys
import codecs
#sys.stdout = codecs.getwriter('utf8')(sys.stdout)

from hmm_prep import *
tweets = xml_to_tagged_tweets('/Users/orion/Google Drive/2016Spring/NLA4ML/gold/MojiSemGold1.xml')
tweets += xml_to_tagged_tweets('/Users/orion/Google Drive/2016Spring/NLA4ML/gold/MojiSemGold2.xml')
tweets += xml_to_tagged_tweets('/Users/orion/Google Drive/2016Spring/NLA4ML/gold/MojiSemGold3.xml')
tweets += xml_to_tagged_tweets('/Users/orion/Google Drive/2016Spring/NLA4ML/gold/MojiSemGold4.xml')
tweets += xml_to_tagged_tweets('/Users/orion/Google Drive/2016Spring/NLA4ML/gold/MojiSemGold5.xml')
tweets += xml_to_tagged_tweets('/Users/orion/Google Drive/2016Spring/NLA4ML/gold/MojiSemGold6.xml')

trainset, testset = split_dataset(tweets, 10)

for klass in ('train','test'):
    fh = codecs.open('crf_'+klass+'.txt','w',encoding='utf8')
    tset = locals()[ klass+'set' ]
    for tweet in tset:
    #for tweet in trainset:
        fh.write("START\tSTART\n")
        for tok in tweet:
            obs, lbl = tok
            line = u'\t'.join([lbl,u'\t'.join(unicode(o) for o in obs)]) #.encode('utf-8')
            fh.write(line+'\n')
            #print(line)
        fh.write("END\tEND\n\n")
    fh.close()



#from nltk.tag.hmm import HiddenMarkovModelTrainer
#hmm_tagger = HiddenMarkovModelTrainer().train(trainset)
#tweet = [x for (x,y) in tweets[290]]
#hmm_tagger.tag(tweet)

#hmm_tagger.test(testset)

