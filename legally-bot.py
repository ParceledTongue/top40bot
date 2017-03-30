#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys, markovify, random

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

model_two = markovify.NewlineText(lyrics, state_size=2)
model_three = markovify.NewlineText(lyrics, state_size=3)
model_four = markovify.NewlineText(lyrics, state_size = 4)
models = [model_two, model_three, model_four]

while True:
  tweet = None
  while tweet == None:
    tweet = random.choice(models).make_short_sentence(140)
  print(tweet)
  api.update_status(tweet)
  time.sleep(60 * 15)
