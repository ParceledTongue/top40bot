#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, tweepy
from lyrics_util import make_lyric

HISTORY_SIZE = 1000

def tweepy_api():
    print('Logging in via tweepy')
    auth = tweepy.OAuthHandler(
            os.environ['TWEEPY_CONSUMER_KEY'], 
            os.environ['TWEEPY_CONSUMER_SECRET'])
    auth.set_access_token(
            os.environ['TWEEPY_ACCESS_KEY'],
            os.environ['TWEEPY_ACCESS_SECRET'])
    return tweepy.API(auth)

def recent_tweets(num, tweepy_api):
    print('Getting most recent ' + str(num) + ' tweets')
    history = set()
    for tweet in tweepy.Cursor(tweepy_api.user_timeline).items(num):
        history.add(tweet.text)
    return history

if __name__ == "__main__":
    tweepy_api = tweepy_api()
    history = recent_tweets(HISTORY_SIZE, tweepy_api)
    print('Composing tweet')
    tweet = None
    while not tweet or tweet in history:
        tweet = make_lyric()
    print('Tweeting: ' + tweet)
    tweepy_api.update_status(tweet)

