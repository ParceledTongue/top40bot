#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = '***REMOVED***'
CONSUMER_SECRET = '***REMOVED***'
ACCESS_KEY = '***REMOVED***'
ACCESS_SECRET = '***REMOVED***'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

to_capitalize = 0
base_tweet = "some say that i'm a pompous creep"
tweet = base_tweet

while to_capitalize < len(tweet):
  to_capitalize += 1
  tweet = tweet = base_tweet
  tweet = tweet[:to_capitalize].capitalize() + tweet[n:]
  while len(tweet) <= 140:
    api.update_status(status=tweet)
    tweet += "!"
    time.sleep(300)

