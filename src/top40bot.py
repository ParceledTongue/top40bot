#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys, markovify, random, datetime, keyconfig
from history import History
from musixmatch import Musixmatch

HISTORY_SIZE = 1500

# login via tweepy 
auth = tweepy.OAuthHandler(keyconfig.tweepy['CONSUMER_KEY'], 
    keyconfig.tweepy['CONSUMER_SECRET'])
auth.set_access_token(keyconfig.tweepy['ACCESS_KEY'], 
    keyconfig.tweepy['ACCESS_SECRET'])
api = tweepy.API(auth)

# build history of most recent HISTORY_SIZE tweets
history = History(HISTORY_SIZE)
old_tweets = []
for tweet in tweepy.Cursor(api.user_timeline).items(HISTORY_SIZE):
  old_tweets.append(tweet.text)
for tweet in reversed(old_tweets):
  history.add(tweet)

model_two = markovify.NewlineText(lyrics, state_size = 2)
model_three = markovify.NewlineText(lyrics, state_size = 3)
model_four = markovify.NewlineText(lyrics, state_size = 4)
models = [model_two, model_three, model_four]

# main loop
while True:
  # prepare the tweet
  tweet = None
  while tweet == None or tweet in history:
    tweet = random.choice(models).make_short_sentence(140)
  # wait until XX:00 to post
  while datetime.datetime.now().time().minute != 0:
    time.sleep(1)
  # post the tweet
  api.update_status(tweet)
  print(tweet)
  history.add(tweet)
  # sleep, but not quite for an hour... we want to prevent timer drift
  time.sleep(60 * 59.5)

