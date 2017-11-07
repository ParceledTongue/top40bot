#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys, markovify, random, datetime as dt, keyconfig, util
from history import History
from musixmatch import Musixmatch

tweet = None
while tweet == None:
  tweet = util.make_tweet()
print(tweet)

