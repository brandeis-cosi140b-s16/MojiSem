from hmm_prep import *
tweets = xml_to_tagged_tweets('/Users/orion/Google Drive/2016Spring/NLA4ML/gold/1.xml')
tweets += xml_to_tagged_tweets('/Users/orion/Google Drive/2016Spring/NLA4ML/gold/2.xml')
tweets += xml_to_tagged_tweets('/Users/orion/Google Drive/2016Spring/NLA4ML/gold/3.xml')
tweets += xml_to_tagged_tweets('/Users/orion/Google Drive/2016Spring/NLA4ML/gold/4.xml')
tweets += xml_to_tagged_tweets('/Users/orion/Google Drive/2016Spring/NLA4ML/gold/5.xml')

trainset, testset = split_dataset(tweets, 10)

for tweet in testset:
    for tok in tweet:
        obs, lbl = tok
        print('\t'.join([lbl,'\t'.join(str(o) for o in obs)]))


#from nltk.tag.hmm import HiddenMarkovModelTrainer
#hmm_tagger = HiddenMarkovModelTrainer().train(trainset)
#tweet = [x for (x,y) in tweets[290]]
#hmm_tagger.tag(tweet)

#hmm_tagger.test(testset)

