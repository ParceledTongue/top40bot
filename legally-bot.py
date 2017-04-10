#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys, markovify, random, datetime

# login via tweepy 
CONSUMER_KEY = '***REMOVED***'
CONSUMER_SECRET = '***REMOVED***'
ACCESS_KEY = '***REMOVED***'
ACCESS_SECRET = '***REMOVED***'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# build set of old tweets
old_tweets = set()                                                          
for tweet in tweepy.Cursor(api.user_timeline).items():
  old_tweets.add(tweet.text)

# generate models
with open("lyrics.txt") as f:
  lyrics = f.read()

model_two = markovify.NewlineText(lyrics, state_size = 2)
model_three = markovify.NewlineText(lyrics, state_size = 3)
model_four = markovify.NewlineText(lyrics, state_size = 4)
models = [model_two, model_three, model_four]

# main loop
while True:
  # prepare the tweet
  tweet = None
  while tweet == None or tweet in old_tweets:
    tweet = random.choice(models).make_short_sentence(140)
  # wait until XX:00 to post
  while datetime.datetime.now().time().minute != 0:
    time.sleep(1)
  # post the tweet
  api.update_status(tweet)
  print(tweet)
  old_tweets.add(tweet)
  # sleep, but not quite for an hour... we want to prevent timer drift
  time.sleep(60 * 59.5)

