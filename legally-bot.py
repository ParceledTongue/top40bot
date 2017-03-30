#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys, markovify

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = '***REMOVED***'
CONSUMER_SECRET = '***REMOVED***'
ACCESS_KEY = '***REMOVED***'
ACCESS_SECRET = '***REMOVED***'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

with open("lyrics.txt") as f:
  lyrics = f.read()

model = markovify.NewlineText(lyrics)

while True:
  api.update_status(model.make_short_sentence(140))
  time.sleep(60 * 30)
