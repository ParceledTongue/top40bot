import feedparser, markovify, os, random
from track import Track

def get_top_tracks(n=40):
    if (n < 1 or n > 100):
        raise ValueError('n must be a number from 1 to 100')
    feed = feedparser.parse('http://www.billboard.com/rss/charts/hot-100')
    track_info_list = feed["items"][0:n]
    return [Track(info['chart_item_title'], info['artist'])
            for info in track_info_list]

def no_duplicate_lines(old_lyrics):
    new_lyrics = ''
    seen = set()
    for line in old_lyrics.splitlines():
        if line not in seen:
            seen.add(line)
            new_lyrics += line + "\n"
    return new_lyrics

def make_lyric():
    all_lyrics = ''
    for track in get_top_tracks(40):
        track_lyrics = track.get_lyrics()
        if track_lyrics:
            all_lyrics += track_lyrics + '\n'
    all_lyrics = no_duplicate_lines(all_lyrics)
    models = [
        markovify.NewlineText(all_lyrics, state_size = 2),
        markovify.NewlineText(all_lyrics, state_size = 3)]

    tweet = None
    while tweet is None:
        tweet = random.choice(models).make_short_sentence(140)
  
    return tweet

