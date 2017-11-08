#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt, os, time, tweepy, util
from history import History

HISTORY_SIZE = 1500
TWEET_PERIOD = dt.timedelta(minutes = 30)

# login via tweepy
print('Logging in via tweepy')
auth = tweepy.OAuthHandler(
        os.environ['TWEEPY_CONSUMER_KEY'], 
        os.environ['TWEEPY_CONSUMER_SECRET'])
auth.set_access_token(
        os.environ['TWEEPY_ACCESS_KEY'], 
        os.environ['TWEEPY_ACCESS_SECRET'])
api = tweepy.API(auth)

# build history of most recent HISTORY_SIZE tweets
print('Building history of most recent ' + str(HISTORY_SIZE) + ' tweets')
history = History(HISTORY_SIZE)
old_tweets = []
for tweet in tweepy.Cursor(api.user_timeline).items(HISTORY_SIZE):
    old_tweets.append(tweet.text)
for tweet in reversed(old_tweets):
    history.add(tweet)

# calculate when to make the first post
next_post_time = dt.datetime.combine(
        dt.date.today(), dt.time()) # midnight on the current day
while next_post_time <= dt.datetime.now():
    next_post_time += TWEET_PERIOD

# we'll always start the main loop by updating the cache
last_cache_update_date = dt.date.min

# main loop
while True:
    # update the cache if we haven't today
    if dt.date.today() > last_cache_update_date:
       util.update_cache()
       last_cache_update_date = dt.date.today()
    # prepare the tweet
    print('Composing tweet')
    tweet = None
    while tweet == None or tweet in history:
        tweet = util.make_tweet()
    print('Queued tweet is: ' + tweet)
    # wait until the scheduled time to post
    delta = (next_post_time - dt.datetime.now()).total_seconds()
    print('Waiting until ' + str(next_post_time))
    time.sleep(delta)
    next_post_time += TWEET_PERIOD
    # post the tweet
    api.update_status(tweet)
    print('Tweeting: ' + tweet)
    history.add(tweet)

