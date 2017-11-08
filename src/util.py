import markovify, os, random
from musixmatch import Musixmatch
from PyLyrics import PyLyrics
from track import Track

# set up Musixmatch API
musixmatch = Musixmatch('***REMOVED***')

def top_40_tracks():
    info_list = musixmatch.chart_tracks_get(1, 40, True) \
            ['message']['body']['track_list']
    return [Track(info) for info in info_list]

def lyrics_for_track(track):
    lyrics = ''
    try:
        lyrics = PyLyrics.getLyrics(
                track.artist.split(' feat.')[0], track.name)
        print('* lyrics obtained via PyLyrics')
    except:
        lyrics = musixmatch.track_lyrics_get(track.tid) \
                ['message']['body']['lyrics']['lyrics_body']
        print('* lyrics obtained via musixmatch')
        lyrics = lyrics.split('...')[0] # remove text watermark
    return lyrics

def make_lyric():
    all_lyrics = ''
    for track in top_40_tracks():
        all_lyrics += lyrics_for_track(track)
    models = [
        markovify.NewlineText(all_lyrics, state_size = 2),
        markovify.NewlineText(all_lyrics, state_size = 3),
        markovify.NewlineText(all_lyrics, state_size = 4)]

    tweet = None
    while tweet is None:
        tweet = random.choice(models).make_short_sentence(140)
  
    return tweet

